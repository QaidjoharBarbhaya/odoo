# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PayuMoneyController(http.Controller):
    @http.route(['/payment/payumoney/return', '/payment/payumoney/cancel', '/payment/payumoney/error'], type='http', auth='public', csrf=False)
    def payu_return(self, **post):
        """ PayUmoney."""
        return werkzeug.utils.redirect('/payment/process')

    @http.route(['/payment/payumoney/webhook'], type='json', auth='public')
    def payu_webhook(self):
        """ Create this webhook record under https://www.payu.in/business/settings/webhooks """
        post = http.request.jsonrequest
        _logger.info(
            'PayUmoney: entering form_feedback with post data %s', pprint.pformat(post))
        if post:
            if post.get('status'):
                post['status'] = post['status'].lower()
            request.env['payment.transaction'].sudo().form_feedback(post, 'payumoney')
