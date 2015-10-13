'''
Ejercicio Herencia

Programa que lee un archivo con los datos de un vehiculo, lo clasifica por su tipo (vehiculo, vehiculo_aereo, vehiculo_espacial),
al final imprime los datos del vehiculo.

Desarrollado por Jacobo Posada Hoyos
Octubre 10 de 2015
'''

# Importar libreria sys para manejo de argumentos de linea de comandos
import sys
# Importar libreria os para acceder a funcionalidades dependientes del Sistema Operativo
import os

# ------------------ Inicio de definicion de constantes y parametros ------------------ #

# Nombre archivo de errores
nombre_archivo_errores = "errores.txt"

# Nombre archivo de registro de operacion del programa
nombre_archivo_registro = "log.txt"

# Extension por defecto
extension_por_defecto = ".txt"


# ------------------ Fin de definicion de constantes y parametros ------------------ #

# ------------------ Inicio de definicion de funciones empleadas ------------------ #

# Funcion que crea un archivo .txt
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True

# Funcion que lee las lineas de un archivo de texto y las devuelve en una lista.
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 

# Funcion que guarda al final del archivo definido la linea especificada. Devuelve True si fue exitoso o False en caso de error.
def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
		return False
		
	return True


# Funcion que guarda un mensaje de error en el archivo errores.txt
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")

# Funcion que guarda un registro de operacion en el archivo log.txt
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")

# Funcion que finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo errores.txt
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()

# Funcion que valida la existencia, nombre y extension de un archivo.
def validar_archivo(nombre_archivo):
	archivo_valido = True
	
	# El archivo.txt debe existir.
	if(os.path.isfile(nombre_archivo) == False):
		print "No existe archivo " + nombre_archivo
		guardar_error("Archivo suministrado no existe.")

	# Validar que el nombre no contenga espacios.
	cantidad_palabras = len(nombre_archivo.split(" "))
	if(cantidad_palabras > 1):
		archivo_valido = False
		guardar_error("Nombre de archivo tiene mas de una palabra.")
	
	# Validar que la extension sea .txt
	if(not nombre_archivo.endswith(extension_por_defecto)):
		archivo_valido = False
		guardar_error("Archivo no tiene extension  " + extension_por_defecto)
	
	return archivo_valido

# Funcion que valida que la estructura de cada linea del archivo vehiculo sea correcta
def validar_linea_archivos_vehiculos (linea_por_validar, numero_de_linea):
	array_respuesta = [0 for x in range(3)]

	# Separar la linea por el simbolo (token) =
	arreglo_propiedades = linea_por_validar.split("=")
	
	if arreglo_propiedades[1][len(arreglo_propiedades[1])-1] == "\n":
		arreglo_propiedades[1] = arreglo_propiedades[1][0:len(arreglo_propiedades[1])-1]
	else:
		arreglo_propiedades[1] = arreglo_propiedades[1]
	
	
	if arreglo_propiedades [0] == "tipo" or arreglo_propiedades[0] == "modelo":
		
		array_respuesta[0] = True
		array_respuesta[1] = arreglo_propiedades[0]
		array_respuesta[2] = arreglo_propiedades[1]
		return array_respuesta
	else:
		array_respuesta [0] = False
	if arreglo_propiedades[0] != "modelo" or arreglo_propiedades[0] != "tipo":
		try:
			propiedades = int(arreglo_propiedades[0])
			guardar_error("La linea " + str(numero_de_linea) + " no cumple con la estructura requerida")
			array_respuesta[0]= False
		except ValueError:
			array_respuesta[0]= True
			array_respuesta[1]= arreglo_propiedades[0]
		valor_propiedades= int(arreglo_propiedades[1])
		if valor_propiedades >0:
			array_respuesta[2] = arreglo_propiedades[1]
		else:
			array_respuesta[0] = False
	return array_respuesta

# ------------------ Fin de definicion de funciones empleadas ------------------ #

#----------------------------Inicializacion de archivos----------------------------#

# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")

# Crear el archivo log.txt para almacenar el registro de operacion del programa.
crear_archivo("log.txt")

guardar_log("Creados archivos errores.txt y log.txt")


#---------------------------------Validaciones----------------------------------#



# Obtener numero de argumentos de linea de comandos
cantidad_argumentos = len(sys.argv)

# Validar que el numero de argumentos sea igual a 2, garantizando que se haya el nombre del archivo del vehiculo.
if (cantidad_argumentos != 2):	
	terminar_programa("Numero de argumentos incorrecto. Debe suministrar un argumento con el archivo del vehiculo")

guardar_log("Numero de argumentos OK")

archivo_vehiculo = sys.argv[1]

# Validacion para el archivo del vehiculo
if validar_archivo(archivo_vehiculo) == False:
	terminar_programa("El archivo no cumple con los requerimientos.")

guardar_log("Archivo OK")


# Variable que almacena el contenido de las lineas del archivo
lineas_archivo = tuple(leer_lineas_archivo(archivo_vehiculo))

# Variable que almacena el numero de lineas del archivo
numero_lineas_archivo = len(lineas_archivo)

# Validar que la estructura de las lineas del archivo sea correcta
for x in range (0, numero_lineas_archivo):
	linea_validada = validar_linea_archivos_vehiculos(lineas_archivo[x], x+1)
	if linea_validada[0] == False:
		terminar_programa('La linea: '+str(lineas_archivo[x])+'no tiene la estructura requerida')

guardar_log("Numero de propiedades OK")


#------------------------Inicio de creacion de clases y metodos---------------------#

class vehiculo:
	def __init__(self, modelo, n_ejes, cc_motor):
		self.modelo = modelo
		self.n_ejes = n_ejes
		self.cc_motor = cc_motor
	
	def mostrar_propiedades(self):
		print '**********Propiedades del vehiculo***********'
		print 'Modelo:'+(self.modelo)
		print 'Numero de ejes:'+str(self.n_ejes)
		print 'Cilindraje:'+str(self.cc_motor)


class vehiculo_aereo(vehiculo):
	def __init__(self, modelo, n_ejes, cc_motor, n_alas, n_alerones, flaps):
		vehiculo.__init__(self, modelo, n_ejes, cc_motor)
		self.n_alas = n_alas
		self.n_alerones = n_alerones
		self.flaps = flaps
		
	def mostrar_propiedades_aereo(self):
		print "***********Propiedades del vehiculo_aereo***********"
		print 'Modelo:'+(self.modelo)
		print 'Numero de ejes:'+str(self.n_ejes)
		print 'Cilindraje:'+str(self.cc_motor)
		print 'Numero de alas:'+str(self.n_alas)
		print 'Numero de alerones:'+str(self.n_alerones)
		print 'Flaps:'+str(self.flaps)

class vehiculo_espacial(vehiculo_aereo):
	def __init__(self, modelo, n_ejes, cc_motor, n_alas, n_alerones, flaps, n_cohetes, capac_astro, tamano_tanque):
		vehiculo_aereo.__init__(self, modelo, n_ejes, cc_motor, n_alas, n_alerones, flaps)
		self.n_cohetes = n_cohetes
		self.capac_astro = capac_astro
		self.tamano_tanque = tamano_tanque
		
	def mostrar_propiedades_espacial(self):
		print "***********Propiedades del vehiculo espacial***********"
		print 'Modelo:'+(self.modelo)
		print 'Numero de ejes:'+str(self.n_ejes)
		print 'Cilindraje:'+str(self.cc_motor)
		print 'Numero de alas:'+str(self.n_alas)
		print 'Numero de alerones:'+str(self.n_alerones)
		print 'Flaps:'+str(self.flaps)
		print 'Numero de cohetes:' +str(self.n_cohetes)
		print 'Capacidad de Astronautas:'+str(self.capac_astro)
		print 'Tamano tanque:'+str(self.tamano_tanque)

#------------------------Fin de creacion de clases y metodos---------------------#

#------------------------Inicio de logica del programa---------------------#

# Separar la primera linea del archivo para conocer el tipo de vehiculo.
array_tipo = lineas_archivo[0].split('=')

if array_tipo[1][len(array_tipo[1])-1] == "\n":
	array_tipo[1] = array_tipo[1][0:len(array_tipo[1])-1]
else:
	array_tipo[1] = array_tipo[1]

# Validar que el tipo de vehiculo sea correcto
if array_tipo[1] != "vehiculo" and array_tipo[1] != "vehiculo_aereo" and array_tipo[1] != "vehiculo_espacial":
	terminar_programa("El tipo de vehiculo no es correcto")

# Camino a seguir si el tipo es un vehiculo
if array_tipo[1] == "vehiculo":
	guardar_log("Tipo de vehiculo:  Vehiculo")
	# Validar que el numero de propiedades sean 4 
	numero_lineas_vehiculo = leer_lineas_archivo(archivo_vehiculo)
	if numero_lineas_archivo < 4 :
		terminar_programa("El numero de propiedades es erroneo")
	array_vehiculo = [1 for t in range(numero_lineas_archivo)]
	for x in range (1, numero_lineas_archivo):
		array = lineas_archivo[x].split('=')
		array_vehiculo[x] = array[1]
	# Se llama la funcion (metodo) propia de la clase y se imprime las propiedades del vehiculo.
	prop_vehiculo = vehiculo(array_vehiculo[1],array_vehiculo[2],array_vehiculo[3])
	guardar_log("Imprimiendo las propiedades del vehiculo")
	prop_vehiculo.mostrar_propiedades()


# Camino a seguir si el tipo es un vehiculo_aereo
if array_tipo[1] == "vehiculo_aereo":
	guardar_log("Tipo de vehiculo:  Vehiculo_Aereo")
	# Validar que el numero de propiedades sean 6 
	numero_lineas_vehiculo = leer_lineas_archivo(archivo_vehiculo)
	if numero_lineas_archivo < 6 :
		terminar_programa("El numero de propiedades es erroneo")
	array_vehiculo = [1 for t in range(numero_lineas_archivo)]
	for x in range (1, numero_lineas_archivo):
		array = lineas_archivo[x].split('=')
		array_vehiculo[x] = array[1]
	# Se llama la funcion (metodo) propia de la clase y se imprime las propiedades del vehiculo.
	prop_vehiculo_aereo = vehiculo_aereo(array_vehiculo[1], array_vehiculo[2], array_vehiculo[3], array_vehiculo[4], array_vehiculo[5], array_vehiculo[6])
	guardar_log("Imprimiendo las propiedades del vehiculo_aereo")
	prop_vehiculo_aereo.mostrar_propiedades_aereo()

# Camino a seguir si el tipo es un vehiculo_espacial
if array_tipo[1] == "vehiculo_espacial":
	guardar_log("Tipo de vehiculo:  Vehiculo_Espacial")
	# Validar que el numero de propiedades sean 9 
	numero_lineas_vehiculo = leer_lineas_archivo(archivo_vehiculo)
	if numero_lineas_archivo < 9 :
		terminar_programa("El numero de propiedades es erroneo")
	array_vehiculo = [1 for t in range(numero_lineas_archivo)]
	for x in range (1, numero_lineas_archivo):
		array = lineas_archivo[x].split('=')
		array_vehiculo[x] = array[1]
	# Se llama la funcion (metodo) propia de la clase y se imprime las propiedades del vehiculo.
	prop_vehiculo_espacial = vehiculo_espacial(array_vehiculo[1], array_vehiculo[2], array_vehiculo[3], array_vehiculo[4], array_vehiculo[5], array_vehiculo[6], array_vehiculo[7], array_vehiculo[8], array_vehiculo[9])
	guardar_log("Imprimiendo las propiedades del vehiculo_espacial")
	prop_vehiculo_espacial.mostrar_propiedades_espacial()


#------------------------Finalizacion del programa---------------------#