from odoo.http import request
from odoo import models, fields, api


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brands'

    name = fields.Char("Brand Name", required=True)
    brand_image = fields.Binary("Brand Image", attachment=True)
    is_website_publish = fields.Boolean("Website Publish")


class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def get_brand(self):
        brands = request.env['product.brand'].search(
            [('is_website_publish', '=', True)])
        if brands:
            return brands
