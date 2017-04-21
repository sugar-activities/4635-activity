#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#   activity.py by:
#       Ignacio Rodríguez <nachoel01@gmail.com>
#   CeibalJAM! - uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
import pango
import shutil
import os
import zipfile
from sugar.datastore import datastore

try:
    shutil.rmtree('/tmp/empaqueta')
except OSError:
    pass

try:
    shutil.copytree('default', '/tmp/empaqueta')
except:
    pass

path = os.path.join('/tmp', 'empaqueta/')
os.remove('/tmp/empaqueta/juego.swf')
for x in os.listdir('/tmp'):
    if 'activity' in x:
	try:
	        shutil.rmtree('/tmp/' + x)
	except:
		os.remove('/tmp/' + x)
    if '.xo' in x:
        os.remove('/tmp/' + x)

from sugar.activity import widgets
from sugar.activity import activity
from sugar.graphics.alert import ErrorAlert
from sugar.graphics.toolbutton import ToolButton
b1 = gtk.STOCK_CANCEL
b2 = gtk.STOCK_OK


class AbrirSVG():
    def __init__(self, entry):
        Ventana = gtk.FileChooserDialog("Abrir icono..",
                 None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (b1, gtk.RESPONSE_CANCEL,
             b2, gtk.RESPONSE_OK))

        Ventana.set_default_response(gtk.RESPONSE_OK)

        Filtro = gtk.FileFilter()
        Filtro.set_name("Imágenes SVG")
        Filtro.add_pattern("*.svg")
        Ventana.add_filter(Filtro)

        Echo = Ventana.run()
        if Echo == gtk.RESPONSE_OK:
            File = Ventana.get_filename()
            entry.set_text(File)
            entry.show_all()
            Ventana.destroy()

        elif Echo == gtk.RESPONSE_CANCEL:
                Ventana.destroy()


class AbrirFLASH():
    def __init__(self, entry):
        Ventana = gtk.FileChooserDialog("Abrir flash..",
                 None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (b1, gtk.RESPONSE_CANCEL,
            b2, gtk.RESPONSE_OK))

        Ventana.set_default_response(gtk.RESPONSE_OK)

        Filtro = gtk.FileFilter()
        Filtro.set_name("Archivo Flash")
        Filtro.add_pattern("*.swf")
        Ventana.add_filter(Filtro)

        Echo = Ventana.run()
        if Echo == gtk.RESPONSE_OK:
            File = Ventana.get_filename()
            entry.set_text(File)
            entry.show_all()
            Ventana.destroy()

        elif Echo == gtk.RESPONSE_CANCEL:
                Ventana.destroy()


class JAMFlash(activity.Activity):

    def __init__(self, handle):
                activity.Activity.__init__(self, handle, True)
                self.toolbar = widgets.ActivityToolbar(self)
                self.buildercanvas = gtk.Builder()
                self.buildercanvas.add_from_file('interfaz.glade')
                self.totl = gtk.EventBox()
                self.totl.modify_bg(gtk.STATE_NORMAL,
                gtk.gdk.color_parse('#282828'))
                self.box = self.buildercanvas.get_object('vbox1')
                self.totl.add(self.box)
                self.box.set_size_request(gtk.gdk.screen_width(),
                gtk.gdk.screen_height() - 55)
                separador = gtk.SeparatorToolItem()
                separador.props.draw = False
                separador.set_expand(True)
                self.img = gtk.Image()
                self.fin = gtk.EventBox()
		p = gtk.gdk.pixbuf_new_from_file_at_size('icons/ceibaljam.svg',
                gtk.gdk.screen_width(), gtk.gdk.screen_height() - 55)
		self.fin.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#282828'))
		self.fin.add(self.img)
                self.img.set_from_pixbuf(p)
                self.button = ToolButton('document-save')
                self.button.set_tooltip('Guardar al diario')
                self.button.connect('clicked', self.save_xo)
                self.toolbar.insert(separador, 1)
                self.toolbar.insert(self.button, 2)
                self.toolbar.insert(separador, 3)

                l = []
                l.append(self.buildercanvas.get_object('label1'))
                l.append(self.buildercanvas.get_object('label2'))
                l.append(self.buildercanvas.get_object('label3'))
                l.append(self.buildercanvas.get_object('label4'))
                l.append(self.buildercanvas.get_object('label5'))
                l.append(self.buildercanvas.get_object('label6'))
                for x in l:
                    x.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                    x.show()

                self.f = self.buildercanvas.get_object('label2')
                self.f.modify_font(pango.FontDescription('15'))
                self.icono = self.buildercanvas.get_object('icono')
                self.flash = self.buildercanvas.get_object('flash')
                self.nombre = self.buildercanvas.get_object('nombre')
                self.bundleid = self.buildercanvas.get_object('bundleid')
                self.version = self.buildercanvas.get_object('version')
                self.version.set_value(1)

                self.btn1 = self.buildercanvas.get_object('btn1')
                self.btn2 = self.buildercanvas.get_object('btn2')
                self.btn1.connect('clicked', self.open, True)
                self.btn2.connect('clicked', self.open, False)

                self.set_canvas(self.totl)
                self.set_toolbar_box(self.toolbar)
                self.show_all()
                self.toolbar.share.props.visible = False

    def save_xo(self, widget):
            if self.flash.get_text() == "":
                alerta = ErrorAlert()
                alerta.props.title = "¿Qué haces?"
                alerta.props.msg = \
                "No puedes hacer una actividad 'flash' sin un flash"
                self.add_alert(alerta)
                alerta.connect('response', self._alert_response_cb)
            if self.nombre.get_text() == "":
                alerta = ErrorAlert()
                alerta.props.title = "Hey!"
                alerta.props.msg = "Escribe un nombre para la actividad."
                self.add_alert(alerta)
                alerta.connect('response', self._alert_response_cb)
            if self.bundleid.get_text() == \
            "Nombredelaactividad" or self.bundleid.get_text() == "":
                alerta = ErrorAlert()
                alerta.props.title = "Hazlo.."
                alerta.props.msg = \
                 "Escribe un 'bundle_id' para la actividad.Si no sabes cual" +\
                 " Simplemente ponle el nombre de la actividad"
                self.add_alert(alerta)
                alerta.connect('response', self._alert_response_cb)
            if self.icono.get_text() != "":
                shutil.copy(self.icono.get_text(), '/tmp/empaqueta/activity/JAMActivityFlash.svg')
            text = """
[Activity]
name = """ + self.nombre.get_text() + """
activity_version = """ + str(int(self.version.get_value())) + """
bundle_id = org.ceibaljam.""" + self.bundleid.get_text() + """
exec = sugar-activity JAMActivityFlash.JAMActivityFlash
icon = JAMActivityFlash
show_launcher = yes
"""

            activityfile = open(os.path.join(path, 'activity', 'activity.info'), 'w')
            activityfile.write(text)
            activityfile.close()
            if self.nombre.get_text() != "" and self.bundleid.get_text() != "" and self.bundleid.get_text() != "Nombredelaactividad" and self.flash != "":
                shutil.copy(self.flash.get_text(), '/tmp/empaqueta/juego.swf')
                new = '/tmp/' + self.nombre.get_text() + '.activity'
                print new
                os.rename(path, new)
                self.box.set_sensitive(False)
                self.set_canvas(self.fin)
                self.show_all()
                self._copy(self.nombre.get_text() + '.activity')
                alerta = ErrorAlert()
                alerta.props.title = "Genial!"
                alerta.props.msg = "La actividad %s ha sido copiada exitosamente al diario." % self.nombre.get_text()
                self.add_alert(alerta)
                alerta.connect('response', self._alert_response_cb)
                self.toolbar.share.props.visible = False

    def compress(self, archivos_a_meter, archivo):
            zipped = zipfile.ZipFile(archivo, mode='a')
            if os.path.isdir(archivos_a_meter):
                    zipped = self.directory(archivos_a_meter, zipped)
            else:
                    zipped.write(archivos_a_meter)

    def directory(self, dirname, zipped):
            for x in os.listdir(dirname):
                    zipped.write(dirname + "/" + x)
                    if os.path.isdir('/tmp/' + dirname + "/" + x):
                        zipped = self.directory(dirname + "/" + x, zipped)
            return zipped

    def _copy(self, path):
        os.chdir('/tmp/')
        pp = self.nombre.get_text() + '.xo'
        file = open(pp, 'w')
        file.close()
        self.compress(path, pp)
        acopiar = datastore.create()
        acopiar.metadata['title'] = pp
        acopiar.metadata['mime_type'] = 'application/vnd.olpc-sugar'
        acopiar.set_file_path('/tmp/' + pp)
        datastore.write(acopiar)
        acopiar.destroy()
        shutil.rmtree(path)
        os.remove(pp)

    def _alert_response_cb(self, alert, response_id):
        self.remove_alert(alert)

    def open(self, widget, svg):
            if svg:
                    AbrirSVG(self.icono)
            else:
                    AbrirFLASH(self.flash)
