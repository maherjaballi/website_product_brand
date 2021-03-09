from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.http_routing.models.ir_http import slug

PPG = 5  # Products Per Page
PPR = 4  # Products Per Row


class WebsiteSaleExt(WebsiteSale):

    def _get_search_domain_ext(self, search, category, attrib_values,
                               brand_values):
        domain = request.website.sale_product_domain()

        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike', srch),
                    ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch),
                    ('product_variant_ids.default_code', 'ilike', srch)]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        if brand_values:
            domain += [('product_brand_id', 'in', brand_values)]

        return domain

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        # For Attributes
        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [list(map(int, v.split("-"))) for v in attrib_list if v]
        attributes_ids = set([v[0] for v in attrib_values])
        attrib_set = set([v[1] for v in attrib_values])

        # For Brands
        brand_list = request.httprequest.args.getlist('brand-id')
        brand_values = [list(map(str, v.split("-"))) for v in brand_list if v]
        brand_set = set([int(v[1]) for v in brand_values])

        Product = request.env['product.template']

        domain = self._get_search_domain_ext(search, category, attrib_values,
                                             list(brand_set))
        keep = QueryURL('/shop', category=category and int(category),
                        search=search, attrib=attrib_list,
                        order=post.get('order'), brands=brand_list)

        url = "/shop"
        if category:
            category = request.env['product.public.category'].browse(
                int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list
        if brand_list:
            post['brands'] = brand_list

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count,
                                      page=page, step=ppg, scope=7,
                                      url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'],
                                  order=self._get_search_order(post))
        ProductAttribute = request.env['product.attribute']
        ProductBrand = request.env['product.brand']
        if products:
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([('attribute_line_ids.product_tmpl_id', 'in', selected_products.ids)])
            prod_brands = []
            for product in selected_products:
                if product.product_brand_id:
                    prod_brands.append(product.product_brand_id.id)
            brands = ProductBrand.browse(list(set(prod_brands)))
        else:
            attributes = ProductAttribute.browse(attributes_ids)
            brands = ProductBrand.browse(brand_set)

        res = super(WebsiteSaleExt, self).shop(page=page, category=category,
                                               search=search, ppg=ppg, **post)

        res.qcontext.update({
            'pager': pager, 'products': products,
            'brands': brands, 'bins': TableCompute().process(products, ppg),
            'attributes': attributes, 'search_count': product_count,
            'attrib_values': attrib_values,
            'brand_values': brand_values, 'brand_set': brand_set,
            'attrib_set': attrib_set,
            'PPG': PPG, 'keep': keep,
        })
        return res