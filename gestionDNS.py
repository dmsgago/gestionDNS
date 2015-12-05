#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, commands

# Comprueba el número de argumentos
def numargs (numero):
    if numero > 0 and numero <= 5:
        return(True)
    else:
        return(False)

# Comprueba el primer parámetro
def primerarg (parametro):
    if parametro == "-h" or parametro == "-a" or parametro == "-b":
        return(True)
    else:
        return(False)

# Comprueba las opciones del parámetro "-a"
def opciones (opcion):
    if opcion == "-dir" or opcion == "-alias":
        return(True)
    else:
        return(False)

# Incluye un nuevo registro "A" y "PTR"
def incluir_reg_a (nombre, ip):
    lista_bytes = ip.split('.')
    registro_a = ('%s IN A %s'%(nombre, ip))
    registro_ptr = ('%s IN PTR %s'%(ip, nombre))
    # Comprueba que la dirección IP del resgistro "PRT" pertenece a la red "10.0.0.0/24"
    commands.getoutput('echo "%s">>/var/cache/bind/db.diego.gn.org'%registro_a)
    if lista_bytes[0] == '10' and lista_bytes[1] == '0' and lista_bytes[2] == '0':
        commands.getoutput('echo "%s">>/var/cache/bind/db.0.0.10'%registro_b)
    # Reinicia el demonio bind9
    commands.getoutput('rndc reload')

# Incluye un nuevo registro "CNAME"
def incluir_reg_cname (alias, nombre):
    registro_cname = ('%s IN CNAME %s'%(alias, nombre))
    commands.getoutput('echo "%s">>/var/cache/bind/db.diego.gn.org'%registro_cname)
    # Reinicia el demonio bind9
    commands.getoutput('rndc reload')

def eliminar_registro (nombre):
    # Almacena el tipo de registro que eliminará
    registro_dir = commands.getoutput('cat /var/cache/bind/db.diego.gn.org|egrep \'^%s \''%nombre)
    registro_ptr = commands.getoutput('cat /var/cache/bind/db.0.0.10|egrep \'.*PTR.*%s\''%nombre)
    atributos = registro_dir.split()
    tipo_registro = atributos[2]
    if tipo_registro == 'A':
        # Almacena los alias que apuntan al registro "A" a eliminar
        alias_de_a = commands.getoutput('cat /var/cache/bind/db.diego.gn.org|egrep \'.*CNAME.*%s\''%nombre).split('\n')
        # Elimina un registro, creando anteriormente una copia de seguridad del fichero "nombrefichero~"
        commands.getoutput('sed -i"~" \'/%s/ d\' /var/cache/bind/db.diego.gn.org'%registro_dir)
        commands.getoutput('sed -i"~" \'/%s/ d\' /var/cache/bind/db.0.0.10'%registro_ptr)
        # Elimina todos los alias que apuntan al registro "A" eliminado
        for alia in alias_de_a:
            commands.getoutput('sed -i"~" \'/%s/ d\' /var/cache/bind/db.diego.gn.org'%alia)
    elif tipo_registro == 'CNAME':
        commands.getoutput('sed -i"~" \'/%s/ d\' /var/cache/bind/db.diego.gn.org'%registro_dir)
    else:
        print("Tipo de registro desconocido: %s"%tipo_registro)
    # Reinicia el demonio bind9
    commands.getoutput('rndc reload')

def ayuda ():
        print '''
    Descripción:
    \tgestionDNS.py es una herramienta desarrollada en python que permite administrar las zonas de resolución de nombre en Bind9.
    Sintaxis:
    \tgestionDNS.py OPCIÓN [TIPO_REGISTRO] NOMBRE [DIRECCIÓN IP]
    Opciones:
    \t-h
    \t\tMuestra la ayuda de gestionDNS.py.
    \t-a
    \t\tAñade un nuevo registo a la zonas de resolución de nombres.
    \t\t-dir
    \t\t\tAñade un registro tipo "A" y actualiza la zona de resolución inversa.
    \t\t-alias
    \t\t\tAñade un registro tipo "CNAME"
    Ejemplo:
    \tgestionDNS.py -a -dir nombre 10.0.0.100
    \tgestionDNS.py -a -alias apodo nombre
    \tgestionDNS.py -b apodo
    '''
        
# Procedimiento principal
if numargs(len(sys.argv)):
    # Comprueba que el primer parámetro del programa sea válido
    if primerarg(sys.argv[1]):
        if sys.argv[1] == '-a':
            # Comprueba las opciones del parámetro -a
            if opciones(sys.argv[2]):
                if sys.argv[2] == '-dir':
                    # Añade un nuevo registro "A" y "PTR"
                    incluir_reg_a(sys.argv[3],sys.argv[4])
                else:
                    # Añade un nuevo registro "CNAME"
                    incluir_reg_cname(sys.argv[3],sys.argv[4])
            else:
                print(' Error. Se esperaba una de las siguientes opciones: "-dir"|"-alias".')
        elif sys.argv[1] == '-b':
            eliminar_registro(sys.argv[2])
        else:
            ayuda()
    else:
        print(' Error. Parámetro desconocido: %s.\n Prueba a utilizar la opción -h para ver la ayuda.'%sys.argv[1])
else:
    print(' Error. Número total de argumentos inválido: %s.'%len(sys.argv))
