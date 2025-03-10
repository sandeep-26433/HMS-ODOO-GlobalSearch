from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DoctorMedicineLines(models.Model):
    _name = 'doctor.medicine.lines'
    _description = 'Medicine Lines'

    appointment_id = fields.Many2one('doctor.appointments', string="Appointment", ondelete='cascade', required=True)
    reference_id = fields.Char(string="Patient Reference ID", readonly=True)
    medicine_id = fields.Many2one('doctor.medicines', string="Medicine", required=True)
    dosage_id = fields.Many2one('doctor.dosages', string="Dosage")
    usage = fields.Text(string="Usage")
    days = fields.Integer(string="Days", required=True, default=1)
    course = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string="Course")
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    prescription_date = fields.Date(string="Prescription Date", default=fields.Date.today)

    @api.model
    def create(self, vals):
        """ Ensure reference_id is copied from appointment_id before creating a record """
        if vals.get('appointment_id'):
            appointment = self.env['doctor.appointments'].browse(vals['appointment_id'])
            if appointment.exists():
                vals['reference_id'] = appointment.reference_id
        return super(DoctorMedicineLines, self).create(vals)

    @api.constrains('days', 'quantity')
    def _check_days_quantity(self):
        """Ensure that Days and Quantity are greater than 0"""
        for record in self:
            if record.days <= 0:
                raise ValidationError("Days must be greater than 0.")
            if record.quantity <= 0:
                raise ValidationError("Quantity must be greater than 0.")
