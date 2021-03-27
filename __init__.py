# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice


def register():
    Pool.register(
        invoice.PostInvoicesStart,
        module='account_invoice_post_wizard', type_='model')
    Pool.register(
        invoice.PostInvoices,
        module='account_invoice_post_wizard', type_='wizard')
