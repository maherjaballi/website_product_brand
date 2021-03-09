{
    # Theme information
    'name': 'Website Product Brand',
    'category': 'Website',
    'summary': 'Filter Products By Brand at Category Page',
    'description': "Filter Products By Brand at Category Page",
    'version': '11.0.1.0.0',
    'author': 'Tecspek',
    # Dependencies
    'depends': [
        'website_sale',
    ],

    # Views
    'data': [
        'security/ir.model.access.csv',
        'template/template.xml',
        'template/assets.xml',
        'view/product_template_brand.xml',
        'view/brand.xml',
    ],
    'support': 'help.tecspek@gmail.com',
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'currency': 'EUR',
}
