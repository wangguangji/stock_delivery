# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields


class vehicle(osv.osv):
    
    _name = 'stock.vehicle'
    
    _description = u"车辆管理"
    
    _columns = {
        'code':fields.char(u'车牌号',required=True),
        'name': fields.char(u'名称',  required=True),
        'load':fields.char(u'载重'),
        'length':fields.char(u'长'),
        'width':fields.char(u'宽'),
        'height':fields.char(u'高'),
        'style':fields.char(u'围栏形式'),
        'description': fields.text(u'描述'),
        'image':fields.binary(u'图片'),
        'partner_id': fields.many2one('res.partner', u'所属承运方',domain="[('delivery','=',True)]"),
    }