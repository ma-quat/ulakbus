# -*-  coding: utf-8 -*-
"""General Core views"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

from pyoko import field
from zengine.lib.forms import JsonForm
from ulakbus.models import Personel


class PersonelEkleForm(JsonForm):
    tckn = field.String("Kimlik No")


def yeni_personel_ekle(current):
    current.output['forms'] = PersonelEkleForm().serialize()


def atama_yap(current):
    pass


def yeni_ekle_kontrol(current):
    pass


def personel_silindi_isaretle(current):
    pass


def personel_aktiflestir(current):
    p = Personel.objects.filter(tckn=current['data']['tckn']).get()
    p.aktif = True
    p.save()
