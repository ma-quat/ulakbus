# -*-  coding: utf-8 -*-

# Copyright (C) 2015 ZetaOps Inc.

__author__ = 'Ozgur Firat Cinar'

from zato.server.service import Service
import os
from time import sleep
import urllib2
import socket

os.environ["PYOKO_SETTINGS"] = 'ulakbus.settings'
from ulakbus.models.hitap import HizmetKayitlari

H_USER = os.environ["HITAP_USER"]
H_PASS = os.environ["HITAP_PASS"]


class HizmetCetveliSorgula(Service):
    """
    HITAP HizmetCetveliSorgula Zato Servisi
    """

    def handle(self):

        def pass_hizmet_kayitlari(hizmet_kayitlari_passed, record_values):
            hizmet_kayitlari_passed.baslama_tarihi = record_values['baslama_tarihi']
            hizmet_kayitlari_passed.bitis_tarihi = record_values['bitis_tarihi']
            hizmet_kayitlari_passed.emekli_derece = record_values['emekli_derece']
            hizmet_kayitlari_passed.emekli_kademe = record_values['emekli_kademe']
            hizmet_kayitlari_passed.gorev = record_values['gorev']
            hizmet_kayitlari_passed.unvan_kod = record_values['unvan_kod']
            hizmet_kayitlari_passed.hizmet_sinifi = record_values['hizmet_sinifi']
            hizmet_kayitlari_passed.kayit_no = record_values['kayit_no']
            hizmet_kayitlari_passed.kazanilmis_hak_ayligi_derece = record_values[
                'kazanilmis_hak_ayligi_derece']
            hizmet_kayitlari_passed.kazanilmis_hak_ayligi_kademe = record_values[
                'kazanilmis_hak_ayligi_kademe']
            hizmet_kayitlari_passed.odeme_derece = record_values['odeme_derece']
            hizmet_kayitlari_passed.odeme_kademe = record_values['odeme_kademe']
            hizmet_kayitlari_passed.emekli_ekgosterge = record_values['emekli_ek_gosterge']
            hizmet_kayitlari_passed.kadro_derece = record_values['kadro_derece']
            hizmet_kayitlari_passed.kazanilmis_hak_ayligi_ekgosterge = record_values[
                'kazanilmis_hak_ayligi_ekgosterge']
            hizmet_kayitlari_passed.odeme_ekgosterge = record_values['odeme_ekgosterge']
            hizmet_kayitlari_passed.sebep_kod = record_values['sebep_kod']
            hizmet_kayitlari_passed.tckn = record_values['tckn']
            try:
                hizmet_kayitlari_passed.ucret = float(record_values['ucret'].strip())
            except ValueError:
                pass
            try:
                hizmet_kayitlari_passed.yevmiye = float(record_values['yevmiye'].strip())
            except ValueError:
                pass
            hizmet_kayitlari_passed.kurum_onay_tarihi = record_values['kurum_onay_tarihi']

        tckn = self.request.payload['personel']['tckn']
        conn = self.outgoing.soap['HITAP'].conn

        # connects with soap client to the HITAP
        try:
            with conn.client() as client:
                service_bean = client.service.HizmetCetvelSorgula(H_USER, H_PASS,
                                                                  tckn).HizmetCetveliServisBean
                self.logger.info("zato service started to work.")

                hitap_dict = {}
                for record in range(0, len(service_bean)):
                    hitap_dict[service_bean[record].kayitNo] = {
                        'baslama_tarihi': '01.01.1900' if
                        service_bean[record].baslamaTarihi == "01.01.0001" else
                        service_bean[record].baslamaTarihi,
                        'bitis_tarihi': '01.01.1900' if
                        service_bean[record].bitisTarihi == "01.01.0001" else
                        service_bean[record].bitisTarihi,
                        'emekli_derece': service_bean[record].emekliDerece,
                        'emekli_kademe': service_bean[record].emekliKademe,
                        'gorev': service_bean[record].gorev,
                        'unvan_kod': service_bean[record].unvanKod,
                        'hizmet_sinifi': service_bean[record].hizmetSinifi,
                        'kayit_no': service_bean[record].kayitNo,
                        'kazanilmis_hak_ayligi_derece': service_bean[
                            record].kazanilmisHakAyligiDerece,
                        'kazanilmis_hak_ayligi_kademe': service_bean[
                            record].kazanilmisHakAyligiKademe,
                        'odeme_derece': service_bean[record].odemeDerece,
                        'odeme_kademe': service_bean[record].odemeKademe,
                        'emekli_ek_gosterge': service_bean[record].emekliEkGosterge,
                        'kadro_derece': service_bean[record].kadroDerece,
                        'kazanilmis_hak_ayligi_ekgosterge': service_bean[
                            record].kazanilmisHakAyligiEkGosterge,
                        'odeme_ekgosterge': service_bean[record].odemeEkGosterge,
                        'sebep_kod': service_bean[record].sebepKod,
                        'tckn': service_bean[record].tckn,
                        'ucret': service_bean[record].ucret,
                        'yevmiye': service_bean[record].yevmiye,
                        'kurum_onay_tarihi': '01.01.1900' if
                        service_bean[record].kurumOnayTarihi == "01.01.0001" else service_bean[
                            record].kurumOnayTarihi
                    }
                self.logger.info("hitap_dict created.")

                # if employee saved before, find that and add new records from hitap to riak
                try:
                    local_records = {}
                    # hizmet_kayitlari_list = HizmetKayitlari.objects.filter(tckn=tckn)
                    for record in HizmetKayitlari.objects.filter(tckn=tckn):
                        local_records[record.kayit_no] = {
                            'baslama_tarihi': record.baslama_tarihi,
                            'bitis_tarihi': record.bitis_tarihi,
                            'emekli_derece': record.emekli_derece,
                            'emekli_kademe': record.emekli_kademe,
                            'gorev': record.gorev,
                            'unvan_kod': record.unvan_kod,
                            'hizmet_sinifi': record.hizmet_sinifi,
                            'kayit_no': record.kayit_no,
                            'kazanilmis_hak_ayligi_derece': record.kazanilmis_hak_ayligi_derece,
                            'kazanilmis_hak_ayligi_kademe': record.kazanilmis_hak_ayligi_kademe,
                            'odeme_derece': record.odeme_derece,
                            'odeme_kademe': record.odeme_kademe,
                            'emekli_ekgosterge': record.emekli_ekgosterge,
                            'kadro_derece': record.kadro_derece,
                            'kazanilmis_hak_ayligi_ekgosterge':
                                record.kazanilmis_hak_ayligi_ekgosterge,
                            'odeme_ekgosterge': record.odeme_ekgosterge,
                            'sebep_kod': record.sebep_kod,
                            'tckn': record.tckn,
                            'ucret': record.ucret,
                            'yevmiye': record.yevmiye,
                            'kurum_onay_tarihi': record.kurum_onay_tarihi
                        }
                    self.logger.info("local_records created.")

                    for record_id, record_values in hitap_dict.items():
                        if record_id in local_records:
                            hizmet_kayitlari = HizmetKayitlari.objects.filter(
                                kayit_no=record_id).get()
                            hizmet_kayitlari.sync = 1
                        else:
                            hizmet_kayitlari = HizmetKayitlari()
                            pass_hizmet_kayitlari(hizmet_kayitlari, record_values)
                            hizmet_kayitlari.sync = 1
                        hizmet_kayitlari.save()

                    for record_id, record_values in local_records.items():
                        hizmet_kayitlari = HizmetKayitlari.objects.filter(
                            kayit_no=record_id).get()
                        if record_id not in hitap_dict:
                            if hizmet_kayitlari.sync == 1:
                                hizmet_kayitlari.sync = 2
                            if hizmet_kayitlari.sync == 2:
                                hizmet_kayitlari.sync = 3

                    self.logger.info("Service runned.")

                except IndexError:
                    hizmet_kayitlari = HizmetKayitlari()
                    for hitap_keys, hitap_values in hitap_dict.items():
                        pass_hizmet_kayitlari(hizmet_kayitlari, hitap_values)
                        hizmet_kayitlari.save()
                        self.logger.info("New HizmetKayitlari saved.")
                    sleep(1)
                except socket.error:
                    self.logger.info("Riak connection refused!")

        except AttributeError:
            self.logger.info("TCKN should be wrong!")
        except urllib2.URLError:
            self.logger.info("No internet connection!")
