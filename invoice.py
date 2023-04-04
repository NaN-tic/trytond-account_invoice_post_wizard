# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.transaction import Transaction
from trytond.pyson import Eval


class PostInvoicesStart(ModelView):
    'Post invoices start'
    __name__ = 'account.invoice.post_invoices.start'

    invoices = fields.Many2Many('account.invoice', None, None, 'Invoices',
        domain=[
            ('state', '=', 'draft'),
            ('company', '=', Eval('company', -1)),
        ], depends=['company'])
    company = fields.Many2One('company.company', 'Company', readonly=True)
    all_invoices = fields.Boolean('All Invoices?')

    def default_company():
        return Transaction().context.get('company', -1)


class PostInvoices(Wizard):
    'Post invoices'
    __name__ = 'account.invoice.post_invoices'

    start = StateView('account.invoice.post_invoices.start',
        'account_invoice_post_wizard.post_invoice_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Post', 'post', 'tryton-ok', default=True),
            ])
    post = StateTransition()

    def _invoice_domain(self):
        return [
            ('state', '=', 'draft'),
            ('company', '=', Transaction().context.get('company', -1)),
            ]

    def transition_post(self):
        Invoice = Pool().get('account.invoice')

        if not self.start.all_invoices:
            Invoice.post(self.start.invoices)
            return 'end'
        invoices = Invoice.search(self._invoice_domain())
        Invoice.post(invoices)
        return 'end'
