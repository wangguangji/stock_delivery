# -*- coding: utf-8 -*-
{
    'name': 'stock_delivery',
    'version': '0.1',
    'category': 'stock',
    'description': """出库单配送信息""",
    'author': 'gavin',
    'sequence': 5,
    'website': 'http://freshfresh.com',
    'depends': ['base','stock','product'],
    'js': [
       ],
    'data': [
         'security/delivery_security.xml',
         'security/ir.model.access.csv',    
         'delivery_view.xml',
         'delivery_sequence.xml',
         'transit_type_view.xml',
         'stock_view.xml',
         'vehicle_view.xml',
    ],
    'installable': True,
}