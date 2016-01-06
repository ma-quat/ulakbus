# -*-  coding: utf-8 -*-

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

from ulakbus.services.personel.hitap.hitap_service import HITAPService


class HizmetAskerlikGetir(HITAPService):
    """
    HITAP HizmetAskerlikGetir Zato Servisi
    """

    def handle(self):
        self.service_name = 'HizmetAskerlikSorgula'
        self.bean_name = 'HizmetAskerlikServisBean'
        self.service_dict = {
            'fields': {
                'tckn': 'Tckn',
                'kayit_no': 'kayitNo',
                'askerlik_nevi': 'askerlikNevi',
                'baslama_tarihi': 'baslamaTarihi',
                'bitis_tarihi': 'bitisTarihi',
                'sayilmayan_gun_sayisi': 'sayilmayanGunSayisi',
                'subay_okulu_giris_tarihi': 'subayOkuluGirisTarihi',
                'astegmen_nasp_tarihi': 'astegmenNaspTarihi',
                'tegmen_nasp_tarihi': 'tegmenNaspTarihi',
                'sinif_okulu_sicil': 'sinifOkuluSicil',
                'muafiyet_neden': 'muafiyetNedeni',
                'gorev_yeri': 'yedekSubayErOgrenimYer',
                'subayliktan_erlige_gecis_tarihi': 'subayliktanErligeGecisTarihi',
                'kita_baslama_tarihi': 'kitaBaslamaTarihi',
                'kita_bitis_tarihi': 'kitaBitisTarihi',
                'kurum_onay_tarihi': 'kurumOnayTarihi'
            },
            'date_filter': ['baslama_tarihi', 'bitis_tarihi', 'subay_okulu_giris_tarihi', 'astegmen_nasp_tarihi',
                            'tegmen_nasp_tarihi', 'subayliktan_erlige_gecis_tarihi', 'kita_baslama_tarihi',
                            'kita_bitis_tarihi', 'kurum_onay_tarihi']
        }
        super(HizmetAskerlikGetir, self).handle()
