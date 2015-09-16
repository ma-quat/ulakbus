# -*-  coding: utf-8 -*-

# Copyright (C) 2015 ZetaOps Inc.

from zato.server.service import Service
import os, urllib2

os.environ["PYOKO_SETTINGS"] = 'ulakbus.settings'
from ulakbus.models.employee import Employee

H_USER = os.environ["HITAP_USER"]
H_PASS = os.environ["HITAP_PASS"]


class HizmetNufusSorgula(Service):
    """
    HITAP HizmetNufusSorgula Zato Servisi
    """

    def handle(self):
        '''
        def pass_nufus_kayitlari(employee_passed_record, record_values):
            nufus_kayitlari = employee_passed_record.NufusKayitlari()
            nufus_kayitlari.tckn = record_values['tckn']
            nufus_kayitlari.ad = record_values['ad']
            nufus_kayitlari.soyad = record_values['soyad']
            nufus_kayitlari.ilk_soy_ad = record_values['ilk_soy_ad']
            try:
                nufus_kayitlari.dogum_tarihi = record_values['dogum_tarihi']
            except ValueError:
                pass
            nufus_kayitlari.cinsiyet = record_values['cinsiyet']
            nufus_kayitlari.emekli_sicil_no = record_values['emekli_sicil_no']
            try:
                nufus_kayitlari.memuriyet_baslama_tarihi = record_values['memuriyet_baslama_tarihi']
            except ValueError:
                pass
            nufus_kayitlari.kurum_sicil = record_values['kurum_sicil']
            nufus_kayitlari.maluliyet_kod = record_values['maluliyet_kod']
            nufus_kayitlari.yetki_seviyesi = record_values['yetki_seviyesi']
            nufus_kayitlari.aciklama = record_values['aciklama']
            try:
                nufus_kayitlari.kuruma_baslama_tarihi = record_values['kuruma_baslama_tarihi']
            except ValueError:
                pass
            try:
                nufus_kayitlari.gorev_tarihi_6495 = record_values['gorev_tarihi_6495']
            except ValueError:
                pass
            nufus_kayitlari.emekli_sicil_6495 = record_values['emekli_sicil_6495']
            nufus_kayitlari.durum = record_values['durum']
            nufus_kayitlari.sebep = record_values['sebep']

            self.logger.info("Nufus kayitlari successfully passed.")
        '''

        tckn = self.request.payload['personel']['tckn']
        conn = self.outgoing.soap['HITAP'].conn

        hitap_dict = {}
        # connects with soap client to the HITAP
        try:
            with conn.client() as client:
                service_bean = client.service.HizmetNufusSorgula(H_USER, H_PASS, tckn)
                self.logger.info("zato service started to work.")

                # collects data from HITAP
                hitap_dict['nufus_sorgula'] = {
                    'tckn': service_bean.tckn,
                    'ad': service_bean.ad,
                    'soyad': service_bean.soyad,
                    'ilk_soy_ad': service_bean.ilkSoyad,
                    'dogum_tarihi': service_bean.dogumTarihi,
                    'cinsiyet': service_bean.cinsiyet,
                    'emekli_sicil_no': service_bean.emekliSicilNo,
                    'memuriyet_baslama_tarihi': service_bean.memuriyetBaslamaTarihi,
                    'kurum_sicil': service_bean.kurumSicili,
                    'maluliyet_kod': service_bean.maluliyetKod,
                    'yetki_seviyesi': service_bean.yetkiSeviyesi,
                    'aciklama': service_bean.aciklama,
                    'kuruma_baslama_tarihi': service_bean.kurumaBaslamaTarihi,
                    'emekli_sicil_6495': service_bean.emekliSicil6495,
                    'gorev_tarihi_6495': '01.01.1900' if
                    service_bean.gorevTarihi6495 == "01.01.0001" else service_bean.gorevTarihi6495,
                    'durum': service_bean.durum,
                    'sebep': service_bean.sebep
                }
                self.logger.info("hitap_dict created.")

                try:
                    self.logger.info("Trying to find object in db if it not exist create.")
                    employee, new = Employee.objects.get_or_create(hitap_dict['nufus_sorgula'],
                                                                   nufus_kayitlari__tckn=tckn)
                    if new:
                        employee.NufusKayitlari(hitap_dict['nufus_sorgula'])
                    if not new:
                        self.logger.info("Personel also in db.")
                    self.logger.info("Personel found in db.")
                    # pass_nufus_kayitlari(employee, hitap_dict['nufus_sorgula'])
                    employee.save()
                    # sleep(1)
                    self.logger.info("Nufus kayitlari successfully saved.")
                    self.logger.info("RIAK KEY: %s " % employee.key)
                finally:
                    self.logger.info("DEBUG")
                '''
                except IndexError:
                    self.logger.info("Personel not found in RIAK DB.")
                    self.logger.info("New personel created.")
                    employee = Employee()
                    employee.tckn = tckn
                    pass_nufus_kayitlari(employee, hitap_dict['nufus_sorgula'])
                    employee.save()
                    # sleep(1)
                    self.logger.info("Nufus kayitlari successfully saved.")
                    self.logger.info("RIAK KEY: %s " % employee.key)
                '''
        except AttributeError:
            self.logger.info("TCKN should be wrong!")

        except urllib2.URLError:
            self.logger.info("No internet connection!")
