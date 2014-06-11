# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields



class stock_delivery(osv.osv):
    _name = 'stock.picking'
    _inherit ='stock.picking'
    
    _columns = {
        'delivery_carrier_id': fields.many2one('stock.delivery.carrier', u'运输公司',select=True), 
        'delivery_id': fields.related('delivery_carrier_id','delivery_id',type='many2one', relation="res.users", string=u"押运人", select=True),
    }
    
class stock_delivery_out(osv.osv):
    
    _inherit ='stock.picking.out'
    
    _columns = {
        'delivery_carrier_id': fields.many2one('stock.delivery.carrier', u'运输公司',select=True), 
        'delivery_id': fields.related('delivery_carrier_id','delivery_id',type='many2one', relation="res.users", string=u"押运人", select=True),
    }
    
        
    def create(self, cr, uid, vals, context=None):
        ids = super(stock_delivery_out, self).create(cr, uid, vals, context=context)
        stock_obj = self.browse(cr,uid,ids)
        if stock_obj.delivery_carrier_id:
            stock_obj.delivery_carrier_id.write({'picking_id':ids})
        return ids
    
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int,long)):
            ids = [ids]
        res = super(stock_delivery_out, self).write(cr, uid, ids, vals, context=context)
        stock_obj = self.browse(cr,uid,ids[0])
        if stock_obj.delivery_carrier_id:
            stock_obj.delivery_carrier_id.write({'picking_id':ids[0]})
        return res
    


class res_partner(osv.osv):
    
    _inherit = 'res.partner'

    _columns = {
        'delivery': fields.boolean(u'承运方'),
        'identity_card':fields.char(u'身份证'),
        'driving_number':fields.char(u'驾驶证'),
        'delivery_image': fields.binary(u'司机图片'),
    }    