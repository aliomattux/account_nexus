from openerp.osv import osv, fields
from openerp import api


class AccountFiscalPosition(osv.osv):
    _inherit = 'account.fiscal.position'
    _columns = {
	'nexus_id': fields.many2one('account.nexus', 'Nexus'),
    }

    @api.v7
    def map_tax(self, cr, uid, fposition, taxes, context=None):
	#In the core code they refer to fposition as an _id when in fact its a browse object
        result = set()

        if not taxes:
            return []

        if not fposition:
            return map(lambda x: x.id, taxes)

	if fposition.nexus_id and fposition.nexus_id.tax_id in taxes:
	    return [fposition.nexus_id.tax_id.id]


	#Begin default functionality

        for t in taxes:
            ok = False
            for tax in fposition_id.tax_ids:
                if tax.tax_src_id.id == t.id:
                    if tax.tax_dest_id:
                        result.add(tax.tax_dest_id.id)
                    ok=True
            if not ok:
                result.add(t.id)
        return list(result)


    def get_fiscal_position(self, cr, uid, company_id, partner_id, delivery_id=None, context=None):
	if not delivery_id or not partner_id:
	    return super(AccountFiscalPosition,self).get_fiscal_position(cr, uid, company_id, partner_id, delivery_id=delivery_id, context=context)

        if not partner_id:
            return False
        partner_obj = self.pool['res.partner']
        partner = partner_obj.browse(cr, uid, partner_id, context=context)

        # partner manually set fiscal position always win
        if partner.property_account_position:
	    print 'Returning'
            return partner.property_account_position.id
        delivery = partner_obj.browse(cr, uid, delivery_id, context=context)

        domains = [[('auto_apply', '=', True), ('vat_required', '=', partner.vat_subjected)]]
        if partner.vat_subjected:
            # Possibly allow fallback to non-VAT positions, if no VAT-required position matches
            domains += [[('auto_apply', '=', True), ('vat_required', '=', False)]]

        for domain in domains:
	    #Check if there is an applicable Nexus
	    if delivery.state_id:
		fiscal_position_ids = self.search(cr, uid, domain + [('nexus_id.state_id', '=', delivery.state_id.id)], context=context, limit=1)
                if fiscal_position_ids:
                    return fiscal_position_ids[0]
            if delivery.country_id.id:
                fiscal_position_ids = self.search(cr, uid, domain + [('country_id', '=', delivery.country_id.id)], context=context, limit=1)
                if fiscal_position_ids:
                    return fiscal_position_ids[0]

                fiscal_position_ids = self.search(cr, uid, domain + [('country_group_id.country_ids', '=', delivery.country_id.id)], context=context, limit=1)
                if fiscal_position_ids:
                    return fiscal_position_ids[0]

        #    fiscal_position_ids = self.search(cr, uid, domain + [('country_id', '=', None), ('country_group_id', '=', None)], context=context, limit=1)
         #   if fiscal_position_ids:
         #       return fiscal_position_ids[0]
        return False
