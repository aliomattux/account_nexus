from openerp.osv import osv, fields


class AccountNexus(osv.osv):
    _name = 'account.nexus'
    _columns = {
	'name': fields.char('Name'),
	'country_id': fields.many2one('res.country', 'Country'),
	'state_id': fields.many2one('res.country.state', 'State'),
	'tax_id': fields.many2one('account.tax', 'Tax'),
	'tax_agency_id': fields.many2one('res.partner', 'Tax Agency'),
    }
