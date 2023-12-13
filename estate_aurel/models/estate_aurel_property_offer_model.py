# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class PropertyOfferModel(models.Model):
    _name = "estate.aurel.property.offer.model"
    _description = "Property Offer Model"

    name = fields.Char('Offer name', required=True)
    price = fields.Float('Price')
    status = fields.Selection(
        string = 'Status',
        copy = False,
        selection = [('A', 'Accepted'), ('R', 'Refused')])
    partner_id = fields.Many2one("estate.aurel.test.model", required=True)
    property_id = fields.Many2one("estate.aurel.test.model", required=True)

    validity = fields.Integer(default = "7")
    deadline = fields.Date(compute="_compute_deadline", inverse="_compute_validity")

    def _compute_validity(self):
        for record in self:
            if record.create_date:
                record.validity = abs((record.deadline - record.create_date.date()).days)
            else:
                record.validity = abs((record.deadline - fields.Date.today()).days)

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.deadline = fields.Date.today() + relativedelta(days=record.validity)



