from openerp.osv import osv, fields


class SaleOrder(osv.osv):
    _inherit = 'sale.order'

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
	vals = super(self, SaleOrder).onchange_partner_id(cr, uid, ids, part, context=context)
	if not vals['partner_shipping_id'] or vals['fiscal_position']:
	    return vals

#	fiscal_position = self.

	return vals
