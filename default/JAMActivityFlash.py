#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMActivityFlash.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
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

from sugar.activity import activity

import gtk, pygtk
pygtk.require("2.0")

import os, string, time, sys, hulahop

from sugar import env

hulahop.startup(os.path.join(env.get_profile_path(), 'gecko'))
from hulahop.webview import WebView

DIRECTORIO_DATOS= os.path.join(activity.get_activity_root(), 'data/')
JUEGO = os.getcwd()+'/juego.swf'

def Crear_Directorio(directorio):
	if not os.path.exists(directorio):
		os.mkdir(directorio)
		os.chmod(directorio, 0666)

Crear_Directorio(DIRECTORIO_DATOS)


class JAMActivityFlash(activity.Activity):
	def __init__(self, handle):
		activity.Activity.__init__(self, handle, False)
		# Toolbar
		c= gtk.HBox()
		c.pack_start(Menu(self), False, False, 0)
		self.set_toolbox(c)

		# Canvas
		caja = gtk.HBox()
		self.set_canvas(caja)

		# Visor Flash
		self.navegador = Navegador()	
		self.navegador.set_web_por_defecto()

		caja.pack_start(self.navegador.get_Navegador(),True,True,0)
        	self.connect("destroy", self.destroy)
		self.show_all()

	def destroy(self, widget=None):
		sys.exit(0)

class Menu(gtk.MenuBar):
# Una barra de Menús # http://developer.gnome.org/pygtk/stable/class-gtkmenubar.html
	def __init__(self, programabase):
		gtk.MenuBar.__init__(self)
		self.programabase= programabase

		# el menu
		self.menu = gtk.Menu()
		self.menu.show()

		# Boton raiz Juegos
		root_menu_juegos = gtk.MenuItem("Juego")
		root_menu_juegos.show()
		root_menu_juegos.set_submenu(self.menu)
		self.append (root_menu_juegos)

		self.set_menu_items()
		self.show_all()

	def set_menu_items(self):
		menu_item = gtk.MenuItem("Salir")
		self.menu.append(menu_item)
		menu_item.connect("activate", self.programabase.destroy)
		menu_item.show()

class Navegador():
	''' Es un Navegador web from hulahop.webview import WebView '''
	def __init__(self):
		self.navegador = None
	
	def get_Navegador(self):
	# Establece la dirección por defecto, y devuelve el navegador para ser incrustado en un contenedor gtk
		self.navegador = WebView()
		self.navegador.load_uri(DIRECTORIO_DATOS+"web.htm")
		return self.navegador
	
	def set_web_por_defecto(self):
	# crea una web para el archivo swf
		htm = """
		<html>
		<head>
		<title>Embedded SWF Player</title>
		</head>
		<body onLoad="resizeTo(1200, 900);">
		<embed src = %s width="1170" height="845"
		   hidden=false autostart=true loop=1>
		</body>
		</html>
		""" % JUEGO

		# Abrir la web creada
		web = open(DIRECTORIO_DATOS+"web.htm", "w")
		web.write(htm)
		web.close()

		try:
		# solo sucede la 1º vez que ejecutas la actividad ya que solo el propietario puede modificar los permisos
			os.chmod(DIRECTORIO_DATOS+"web.htm", 0666)
		except:
			pass
