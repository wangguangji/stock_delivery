# -*- coding: utf-8 -*-
from openerp.osv import fields,osv

class delivery_carrier(osv.osv):
    
    _name = "stock.delivery.carrier"
    
    _description = "运费"

    def get_pay_amount(self, cr, uid, ids, field_name, arg=None, context=None):
        res={}
        if context is None:
            context = {}
        for carrier in self.browse(cr, uid, ids, context=context):
            cr.execute('select sum(amount) from pay_amount_move where carrier_id=%s',(carrier.id,))
            res[carrier.id]=cr.fetchone()[0] or 0.0
        return res
    
    def get_un_pay_amount(self, cr, uid, ids, field_name, arg=None, context=None):
        res={}
        if context is None:
            context = {}
        for carrier in self.browse(cr, uid, ids, context=context):
            res[carrier.id]=carrier.amount -carrier.pay_amount 
        return res
    

    _columns = {
        'code':fields.char(u'运单号',size=64,select=True),        
        'name': fields.char(u'编号', size=64, required=True ,states={'done':[('readonly', True)],}),
        'send_date':fields.datetime(u'发货日期',required=True,states={'done':[('readonly', True)],}),
        'picking_id':fields.many2one('stock.picking',u'出库单',select=True,readonly=True,states={'done':[('readonly', True)],}),
        'delivery_id': fields.many2one('res.users', u'押运人',select=True,states={'done':[('readonly', True)],}),
        'partner_id': fields.many2one('res.partner', u'承运方', required=True,states={'done':[('readonly', True)],}),
        'linkman':fields.many2one('res.partner',u'承运方司机',states={'done':[('readonly', True)],}),
        'type_id':fields.many2one('stock.transite.type',u'运输类型',states={'done':[('readonly', True)],}),
        'vehicle_id':fields.many2one('stock.vehicle',u'车辆',states={'done':[('readonly', True)],}),
        'length': fields.related('vehicle_id','length',type='char', string=u"长度",readonly=True),
        'vehicle_code': fields.related('vehicle_id','code',type='char', string=u"车牌号",readonly=True),
        'width': fields.related('vehicle_id','width',type='char', string=u"宽度",readonly=True),
        'height': fields.related('vehicle_id','height',type='char', string=u"高度",readonly=True),
        'style': fields.related('vehicle_id','style',type='char', string=u"围栏形式",readonly=True),
        'load': fields.related('vehicle_id','load',type='char', string=u"载重",readonly=True),
        'description': fields.text(u'描述'),
        'amount' : fields.float(u'运费金额' ,states={'done':[('readonly', True)],}),
        'pay_amount' : fields.function(get_pay_amount, string=u'已支付金额'),
        'un_pay_amount':fields.function(get_un_pay_amount,string=u'未支付金额'),
        'pay_lines': fields.one2many('pay.amount.move', 'carrier_id', '付款明细',states={'done':[('readonly', True)],}),
        'state': fields.selection([
            ('draft', u'草稿'),
            ('done', u'完成'),
            ], u'状态', readonly=True, select=True, track_visibility='onchange',
        ),
    }
    
    _defaults = {
        'name': '/',
        'state': 'draft',
    }
    
    def action_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'done',})
        return True
    
    def create(self, cr, uid, vals, context=None):
        if not 'name' in vals or vals['name'] == '/':
            vals['name'] = self.pool.get('ir.sequence').get(
                    cr, uid, 'stock.delivery.carrier')
        return super(delivery_carrier, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        carrier_without_code = self.search(
                cr, uid,
                [('name', 'in', [False, '/']),
                 ('id', 'in', ids)],
                context=context)
        direct_write_ids = set(ids) - set(carrier_without_code)
        super(delivery_carrier, self).write(cr, uid,
                                           list(direct_write_ids),
                                           vals, context=context)
        for carrier_id in carrier_without_code:
            vals['name'] = self.pool.get('ir.sequence').get(
                    cr, uid, 'stock.delivery.carrier')
            super(delivery_carrier, self).write(cr, uid,
                                               carrier_id,
                                               vals,
                                               context=context)
        return True
    
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        delivery = self.read(cr, uid, id, ['name'], context=context)
        if delivery['name']:
            default.update({
                'name': delivery['name'] + _('-copy'),
            })
        return super(delivery_carrier, self).copy(cr, uid, id, default, context)
    
    
    def onchange_vehicle_id(self, cr, uid, ids, vehicle_id=False):
        if not vehicle_id:
            return {}
        if vehicle_id:
            vehicle_obj = self.pool.get('stock.vehicle').browse(cr, uid, vehicle_id)
            result = {
                'length': vehicle_obj.length,
                'width': vehicle_obj.width,
                'height': vehicle_obj.height,
                'style' :vehicle_obj.style, 
                'load' : vehicle_obj.load,
                'vehicle_code':vehicle_obj.code,
            }
            return {'value': result}
    

class pay_amount_move(osv.osv):
    
    _name = "pay.amount.move"
    
    _description = u"付款记录"

    _columns = {
        'operator_id': fields.many2one('res.users', u'操作人', required=True),
        'pay_type': fields.char(u'支付方式',select=True),
        'pay_date': fields.datetime(u'支付日期',select=True),
        'amount' : fields.float(u'付款金额'),
        'remark': fields.char(u'备注',select=True),
        'carrier_id': fields.many2one('stock.delivery.carrier', u'运费', select=True,),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
