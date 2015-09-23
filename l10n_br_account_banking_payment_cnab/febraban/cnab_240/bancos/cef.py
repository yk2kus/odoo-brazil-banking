# coding: utf-8
# ###########################################################################
#
#    Author: Luis Felipe Mileo
#            Fernando Marcato Rodrigues
#            Daniel Sadamo Hirayama
#    Copyright 2015 KMEE - www.kmee.com.br
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from ..cnab_240 import Cnab240
import re
import string


class Cef240(Cnab240):

    def __init__(self):
        super(Cnab240, self).__init__()
        from cnab240.bancos import cef
        self.bank = cef

    def _prepare_header(self):
        """

        :return:
        """
        vals = super(Cef240, self)._prepare_header()
        vals['cedente_agencia_conta_dv'] = str(
            vals['cedente_agencia_conta_dv'])
        vals['cedente_codigo_agencia_digito'] = str(
            vals['cedente_codigo_agencia_digito']),
        return vals

    def _prepare_segmento(self, line):
        """

        :param line:
        :return:
        """
        vals = super(Cef240, self)._prepare_segmento(line)

        carteira, nosso_numero, digito = self.nosso_numero(
            line.move_line_id.transaction_ref)

        vals['cedente_agencia_conta_dv'] = str(
            vals['cedente_agencia_conta_dv'])
        vals['identificacao_titulo'] = unicode(str(
            vals['numero_documento']), "utf-8") # Informar o Número do Documento - Seu Número (mesmo das posições 63-73 do Segmento P)

        vals['carteira_numero'] = int(carteira)
        vals['nosso_numero'] = int(nosso_numero)
        vals['nosso_numero_dv'] = int(digito)

        return vals

    # Override cnab_240.nosso_numero. Diferentes números de dígitos entre CEF e Itau
    def nosso_numero(self, format):
        digito = format[-1:]
        carteira = 14
        nosso_numero = re.sub(
            '[%s]' % re.escape(string.punctuation), '', format[3:-1] or '')
        return carteira, nosso_numero, digito
