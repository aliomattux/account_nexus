from openerp.osv import osv, fields


class AccountFiscalPosition(osv.osv):
    _inherit = 'account.fiscal.position'
    _columns = {
	'nexus_id': fields.many2one('account.nexus', 'Nexus'),
    }
