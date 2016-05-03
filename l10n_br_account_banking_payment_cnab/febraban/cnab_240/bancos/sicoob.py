# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from ..cnab_240 import Cnab240
import re
import string


class Sicoob240(Cnab240):

    def __init__(self):
        super(Cnab240, self).__init__()
        from cnab240.bancos import sicoob
        self.bank = sicoob

    def _prepare_header(self):
        vals = super(Sicoob240, self)._prepare_header()
        vals['controlecob_numero'] = '01'# TODO gerar número apropriado
        vals['controlecob_data_gravacao'] = self.data_hoje()
        return vals

    def _prepare_segmento(self, line):
        vals = super(Sicoob240, self)._prepare_segmento(line)

        carteira, nosso_numero, digito = self.nosso_numero(
            line.move_line_id.transaction_ref)

        vals['cedente_dv_ag_cc'] = int(
            vals['cedente_dv_ag_cc'])
        vals['carteira_numero'] = int(carteira)
        vals['nosso_numero'] = int(nosso_numero)
        vals['nosso_numero_dv'] = int(digito)
        vals['prazo_baixa'] = '0'
        vals['controlecob_data_gravacao'] = self.data_hoje()
        return vals

    def nosso_numero(self, format):
        digito = format[-1:]
        carteira = format[:3]
        nosso_numero = re.sub(
            '[%s]' % re.escape(string.punctuation), '', format[3:-1] or '')
        return carteira, nosso_numero, digito
