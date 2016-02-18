# -*-  coding: utf-8 -*-

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

"""Öğrencilerin Genel Bilgileri ile ilgili İş Akışlarına ait
sınıf ve metotları içeren modüldür.

Kimlik Bilgileri, İletişim Bilgileri ve Önceki Eğitim Bilgileri gibi
iş akışlarının yürütülmesini sağlar.

"""

from collections import OrderedDict
from zengine.forms import fields
from zengine import forms
from zengine.views.crud import CrudView
from ulakbus.services.zato_wrapper import MernisKimlikBilgileriGetir
from ulakbus.services.zato_wrapper import KPSAdresBilgileriGetir
from ulakbus.models.ogrenci import Ogrenci, OgrenciProgram, Program, Donem, DonemDanisman
from ulakbus.models.personel import Personel
from ulakbus.views.ders.ders import prepare_choices_for_model


class KimlikBilgileriForm(forms.JsonForm):
    """
    ``KimlikBilgileri`` sınıfı için form olarak kullanılacaktır. Form,
    include listesinde, aşağıda tanımlı alanlara sahiptir.

    """

    class Meta:
        include = ['tckn', "ad", "soyad", "cinsiyet", "dogum_tarihi", "dogum_yeri", "uyruk",
                   "medeni_hali", "baba_adi", "ana_adi",
                   "cuzdan_seri", "cuzdan_seri_no", "kayitli_oldugu_il", "kayitli_oldugu_ilce",
                   "kayitli_oldugu_mahalle_koy",
                   "kayitli_oldugu_cilt_no", "kayitli_oldugu_aile_sıra_no",
                   "kayitli_oldugu_sira_no", "kimlik_cuzdani_verildigi_yer",
                   "kimlik_cuzdani_verilis_nedeni", "kimlik_cuzdani_kayit_no",
                   "kimlik_cuzdani_verilis_tarihi"]

    kaydet = fields.Button("Kaydet", cmd="save")
    mernis_sorgula = fields.Button("Mernis Sorgula", cmd="mernis_sorgula")


class KimlikBilgileri(CrudView):
    """Kimlik Bilgileri İş Akışı

    Kimlik Bilgileri iş akışı 3 adımdan olusmaktadır.

    * Kimlik Bilgileri Formu
    * Mernis Kimlik Sorgulama
    * Kimlik Bilgileri Kaydet

    Bu iş akışımda kullanılan metotlar şu şekildedir:

    Kimlik Bilgilerini Listele:
        CrudView list metodu kullanılmıştır.Kimlik Bilgileri formunu
        listeler.

    Mernis'ten Kimlik Bilgilerini Getir:
        MERNİS, merkezi nüfus idare sisteminin kısa proje adıdır. Bu metot sayesinde
        öğrenciye ait kimlik bilgilerine MERNİS'ten erişilir. KimlikBilgileriForm'undaki
        alanlar MERNİS'ten gelen bilgiler doğrultusunda doldurulur.

    Kaydet:
        MERNİS'ten gelen bilgileri ve yetkili kişinin öğrenciyle girdiği bilgileri
        kaydeder. Bu adım ``CrudView.save()`` metodunu kullanır. İş akışı bu adımdan
        sonra sona erer.

    Bu sınıf ``CrudView`` extend edilerek hazırlanmıştır. Temel model ``Ogrenci``
    modelidir. Meta.model bu amaçla kullanılmıştır.

    Adımlar arası geçiş manuel yürütülmektedir.

    """

    class Meta:
        model = "Ogrenci"

    def kimlik_bilgileri(self):
        """Kimlik Bilgileri Formu"""

        self.form_out(KimlikBilgileriForm(self.object, current=self.current))

    def mernis_sorgula(self):
        """Mernis Sorgulama

        Zato wrapper metodlarıyla Mernis servisine bağlanır, servisten dönen
        değerlerle nesneyi doldurup kaydeder.

        """

        servis = MernisKimlikBilgileriGetir(tckn=self.object.tckn)
        kimlik_bilgisi = servis.zato_request()
        self.object(**kimlik_bilgisi)
        self.object.save()


class IletisimBilgileriForm(forms.JsonForm):
    """
    ``İletişimBilgileri`` sınıfı için form olarak kullanılacaktır. Form,
    include listesinde, aşağıda tanımlı alanlara sahiptir.

    """

    class Meta:
        include = ["ikamet_il", "ikamet_ilce", "ikamet_adresi", "adres2", "posta_kodu", "e_posta", "e_posta2", "tel_no",
                   "gsm"]

    kaydet = fields.Button("Kaydet", cmd="save")
    kps_sorgula = fields.Button("KPS Sorgula", cmd="kps_sorgula")


class IletisimBilgileri(CrudView):
    """İletişim Bilgileri İş Akışı

   İletişim Bilgileri iş akışı 3 adımdan oluşmaktadır.

   * İletisim Bilgileri Formu
   * KPS Adres Sorgulama
   * Iletisim Bilgileri Kaydet

   Bu iş akışında kullanılan metotlar şu şekildedir.

   İletişim Bilgilerini Listele:
      CrudView list metodu kullanılmıştır. İletişim Bilgileri formunu
      listeler.

   KPS Adres Bilgilerini Getir:
      Bu metot sayesinde öğrenciye ait yerleşim yeri bilgilerine merkezi
      Kimlik Paylaşım Sistemi üzerinden erişilir.

      Iletişim Bilgileri formundaki alanlar KPS'ten gelen bilgiler
      doğrultusunda doldurulur.

    Kaydet:
      KPS'ten gelen bilgileri ya da yetkili kişinin öğrenciyle ilgili girdiği
      bilgileri kaydeder. Bu adım ``CrudView.save()`` metodunu kullanır.
      İş akışı bu adımdan sonra sona erer.

    Bu sınıf ``CrudView`` extend edilerek hazırlanmıştır. Temel model ``Ogrenci``
    modelidir. Meta.model bu amaçla kullanılmıştır.

    Adımlar arası geçiş manuel yürütülmektedir.

    """

    class Meta:
        model = "Ogrenci"

    def iletisim_bilgileri(self):
        """İletişim Bilgileri Formu"""

        self.form_out(IletisimBilgileriForm(self.object, current=self.current))

    def kps_sorgula(self):
        """KPS Sorgulama

        Zato wrapper metodlarıyla KPS servisine bağlanır, servisten dönen
        değerlerle nesneyi doldurup kaydeder.

        """
        servis = KPSAdresBilgileriGetir(tckn=self.object.tckn)
        iletisim_bilgisi = servis.zato_request()
        self.object(**iletisim_bilgisi)
        self.object.save()


class OncekiEgitimBilgileriForm(forms.JsonForm):
    """
    ``OncekiEgitimBilgileri`` sınıfı  için object form olarak kullanılacaktır. Form,
    include listesinde, aşağıda tanımlı alanlara sahiptir.

    """

    class Meta:
        include = ["okul_adi", "diploma_notu", "mezuniyet_yili"]

    kaydet = fields.Button("Kaydet", cmd="save")


class OncekiEgitimBilgileri(CrudView):
    """Önceki Eğitim Bilgileri İş Akışı

   Önceki Eğitim Bilgileri iş akışı 2 adımdan oluşmaktadır.

   * Önceki Eğitim Bilgileri Formu
   * Önceki Eğitim Bilgilerini Kaydet

   Bu iş akışında  kullanılan metotlar şu şekildedir:

   Önceki Eğitim Bilgileri Formunu Listele:
      CrudView list metodu kullanılmıştır. Önceki Eğitim Bilgileri formunu listeler.

   Kaydet:
      Girilen önceki eğitim bilgilerini kaydeder. Bu adım ``CrudView.save()`` metodunu kullanır.
      İş akışı bu adımdan sonra sona erer.

   Bu sınıf ``CrudView`` extend edilerek hazırlanmıştır. Temel model ``OncekiEgitimBilgisi``
   modelidir. Meta.model bu amaçla kullanılmıştır.

   Adımlar arası geçiş manuel yürütülmektedir.

    """

    class Meta:
        model = "OncekiEgitimBilgisi"

    def onceki_egitim_bilgileri(self):
        """Önceki Eğitim Bilgileri Formu"""

        self.form_out(OncekiEgitimBilgileriForm(self.object, current=self.current))


def ogrenci_bilgileri(current):
    """Öğrenci Genel Bilgileri

    Öğrenci Genel Bilgileri, öğrencilerin kendi bilgilerini görüntüledikleri
    tek adımlık bir iş akışıdır.

    Bu metod tek adımlık bilgi ekranı hazırlar.

    """

    current.output['client_cmd'] = ['show', ]
    ogrenci = Ogrenci.objects.get(user_id=current.user_id)

    # ordered tablo için OrderedDict kullanılmıştır.
    kimlik_bilgileri = OrderedDict({})
    kimlik_bilgileri.update({'Ad Soyad': "%s %s" % (ogrenci.ad, ogrenci.soyad)})
    kimlik_bilgileri.update({'Cinsiyet': ogrenci.cinsiyet})
    kimlik_bilgileri.update({'Kimlik No': ogrenci.tckn})
    kimlik_bilgileri.update({'Uyruk': ogrenci.tckn})
    kimlik_bilgileri.update({'Doğum Tarihi': '{:%d.%m.%Y}'.format(ogrenci.dogum_tarihi)})
    kimlik_bilgileri.update({'Doğum Yeri': ogrenci.dogum_yeri})
    kimlik_bilgileri.update({'Baba Adı': ogrenci.baba_adi})
    kimlik_bilgileri.update({'Anne Adı': ogrenci.ana_adi})
    kimlik_bilgileri.update({'Medeni Hali': ogrenci.medeni_hali})

    iletisim_bilgileri = {
        'Eposta': ogrenci.e_posta,
        'Telefon': ogrenci.tel_no,
        'Sitem Kullanıcı Adı': current.user.username
    }

    current.output['object'] = [
        {
            "title": "Kimlik Bilgileri",
            "type": "table",
            "fields": kimlik_bilgileri
        },
        {
            "title": "İletişim Bilgileri",
            "type": "table",
            "fields": iletisim_bilgileri
        }
    ]


class ProgramSecimForm(forms.JsonForm):
    """
    ``DanismanAtama`` sınıfı için form olarak kullanılacaktır.

    """

    sec = fields.Button("Seç")


class DanismanSecimForm(forms.JsonForm):
    """
    ``DanismanAtama`` sınıfı için form olarak kullanılacaktır.

    """

    sec = fields.Button("Kaydet")


class DanismanAtama(CrudView):
    """Danışman Atama

    Öğrencilere danışman atamalarının yapılmasını sağlayan workflowa ait
    metdodları barındıran sınıftır.

    """

    class Meta:
        model = "OgrenciProgram"

    def program_sec(self):
        """Program Seçim Adımı

        Programlar veritabanından çekilip, açılır menu içine
        doldurulur.

        """
        guncel_donem = Donem.objects.filter(guncel=True)[0]
        ogrenci_id = self.current.input['id']
        self.current.task_data['ogrenci_id'] = ogrenci_id
        self.current.task_data['donem_id'] = guncel_donem.key

        _form = ProgramSecimForm(current=self.current, title="Öğrenci Programı Seçiniz")
        _choices = prepare_choices_for_model(OgrenciProgram, ogrenci_id=ogrenci_id)
        _form.program = fields.Integer(choices=_choices)
        self.form_out(_form)

    def danisman_sec(self):
        program_id = self.current.input['form']['program']
        donem_id = self.current.task_data['donem_id']
        self.current.task_data['program_id'] = program_id

        program = OgrenciProgram.objects.get(program_id)

        _form = DanismanSecimForm(current=self.current, title="Danışman Seçiniz")
        _choices = prepare_choices_for_model(DonemDanisman, donem_id=donem_id, bolum_id=program.program.bolum.key)
        _form.donem_danisman = fields.Integer(choices=_choices)
        self.form_out(_form)

    def danisman_kaydet(self):
        program_id = self.current.task_data['program_id']
        donem_danisman_id = self.input['form']['donem_danisman']

        o = DonemDanisman.objects.get(donem_danisman_id)
        personel = o.okutman.personel

        self.current.task_data['personel_id'] = personel.key

        ogrenci_program = OgrenciProgram.objects.get(program_id)
        ogrenci_program.danisman = personel
        ogrenci_program.save()

    def kayit_bilgisi_ver(self):
        ogrenci_id = self.current.task_data['ogrenci_id']
        personel_id = self.current.task_data['personel_id']

        ogrenci = Ogrenci.objects.get(ogrenci_id)
        personel = Personel.objects.get(personel_id)

        self.current.output['msgbox'] = {
            'type': 'info', "title": 'Danışman Ataması Yapıldı',
            "msg": '%s adlı öğrenciye %s adlı personel danışman olarak atandı' % (ogrenci, personel)
        }
