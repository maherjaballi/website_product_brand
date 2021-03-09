from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one("product.brand", "Product Brand")
