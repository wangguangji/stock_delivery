# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields

class transit_type(osv.osv):
    
    _name = 'stock.transite.type'
    
    _description = u"运输类型"
    
    _columns = {
        'name': fields.char(u'名称', size=64, required=True),
    }