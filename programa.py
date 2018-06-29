import os.path as path
import os
from typing import TextIO, List, Dict

def inicio(valor):
    if valor:
        with open('archivosdetexto/actividades.txt','w') as arcactividades:
            arcactividades.write("#Archivo de actividades:\n#(formato):\n#ID de actividad,letra\n#Nombre de actividad\n#+\n#ID de quien pago, monto\n#-\n#ID de quien debe, monto, val\n#...\n#(aclaracion1) letra = A si no fue saldada, letra = B si fue saldada\n#(aclaracion2) val = 1 si no se pago, val = 0 si se pago\n#*(separador)\n")

def contador(arcusuarios: TextIO) -> int:
    cont = 0
    linea = arcusuarios.readline()
    while linea.startswith("#"):
        linea = arcusuarios.readline()
    for linea in arcusuarios:
        if linea.startswith('*'):
            cont += 1
    return cont

def crearusuario(datos: list)->None:
    if not path.exists('archivosdetexto/usuarios.txt'):
        with open('archivosdetexto/usuarios.txt','w') as arcusuaruarios:
            arcusuaruarios.write("#Formato:\n#nombre de usuario\n#contrasena usuario\n#email de usuario\n#numero id usuario\n#*(separador de usuarios)\n")
            i = 0
            while i<= 2:
                datos[i] += '\n'
                arcusuaruarios.write(datos[i])
                i += 1
            arcusuaruarios.write('U1\n*\n')
    elif path.exists('archivosdetexto/usuarios.txt'):
        with open('archivosdetexto/usuarios.txt','r') as arcusuaruarios:
            numeroid = contador(arcusuaruarios) + 1
        with open('archivosdetexto/usuarios.txt','a') as arcusuaruarios:
            i = 0
            while i<= 2:
                datos[i] += '\n'
                arcusuaruarios.write(datos[i])
                i += 1
            arcusuaruarios.write('U'+str(numeroid))
            arcusuaruarios.write('\n*\n')

def gestiondeusuario(arcdeusuario: TextIO)-> list:
    arc = arcdeusuario.readline()
    while arc.startswith('#'):
        arc = arcdeusuario.readline()
    lista = arc.split(sep = ',')
    lista[4] = lista[4].strip()
    bandera, nombreusuario, contrasena, mailusuario, idusuario = lista
    if not int(bandera):
        list = lista[1:4]
        crearusuario(list)
    return lista[1:3]

def buscarusuario(nombreycontrasena: list) -> list: #Recibe una lista con nombre y contrasena
    if not path.exists('archivosdetexto/usuarios.txt'):
        retornodatos = ['Nada']
    if path.exists('archivosdetexto/usuarios.txt'):
        with open('archivosdetexto/usuarios.txt','r') as arcdeusuarios:
            linea = arcdeusuarios.readline()
            while linea.startswith('#'):
                linea = arcdeusuarios.readline()
            retornodatos = []
            nombre = linea.strip()
            contrasena = arcdeusuarios.readline().strip()
            email = arcdeusuarios.readline().strip()
            id = arcdeusuarios.readline().strip()
            asterisco = arcdeusuarios.readline().strip()
            if nombreycontrasena[0] == nombre and nombreycontrasena[1] == contrasena:
                retornodatos.append(nombre)
                retornodatos.append(contrasena)
                retornodatos.append(email)
                retornodatos.append(id)
                return retornodatos
            else:
                while (not nombre == nombreycontrasena[0]) and (not nombre == ''):
                    nombre = arcdeusuarios.readline().strip()
                    contrasena = arcdeusuarios.readline().strip()
                    email = arcdeusuarios.readline().strip()
                    id = arcdeusuarios.readline().strip()
                    asterisco = arcdeusuarios.readline().strip()
                if  nombreycontrasena[0] == nombre and nombreycontrasena[1] == contrasena:
                    retornodatos.append(nombre)
                    retornodatos.append(contrasena)
                    retornodatos.append(email)
                    retornodatos.append(id)
                    return retornodatos
                elif nombreycontrasena[0] == nombre:
                    retornodatos.append('Contrasena incorrecta')
                elif retornodatos == []:
                    retornodatos.append('Nada')

                    return retornodatos
    return retornodatos

def generararcdeusuario(temporaldeusuario: TextIO) -> None:
    linea = temporaldeusuario.readline()
    while linea.startswith('#'):
        linea = temporaldeusuario.readline()
    datos = linea.split(',')
    datos[1] = datos[1].strip()
    datosregistrados = buscarusuario(datos)
    if datos[0] == datosregistrados[0]:
        with open('archivosdetexto/archivodeusuario.txt','w') as archivodeusuario:
            archivodeusuario.write("#Formato:\n#bandera,nombreusuario,contrasena,mailusuario,idusuario\n")
            archivodeusuario.write('1,')
            i = 0
            while i <= 2:
                archivodeusuario.write(datosregistrados[i] + ',')
                i += 1
            archivodeusuario.write(datosregistrados[i])
    elif datosregistrados[0] == 'Contrasena incorrecta':
        print(datosregistrados[0])
        alerta = 19 #Pongo una alerta que vuelve a pedir contrasena
    else:
        print("Generar nuevo usuario, Ingrese email:",end = "")
        mail = 'fabroghilardini@gmail.com'
        datos.append(mail)
        with open('archivosdetexto/archivodeusuario.txt','w') as archivodeusuario:
            archivodeusuario.write("#Formato:\n#bandera,nombreusuario,contrasena,mailusuario,idusuario\n")
            archivodeusuario.write("0,")
            for dato in datos:
                archivodeusuario.write(dato + ',')
            archivodeusuario.write('None')

def quienmedebe(actividades: TextIO,idusuario: str) -> Dict[str, float]:
    linea = actividades.readline()
    dictdeudores = {}
    while not (linea == ''):
        while linea.startswith('#') or linea.startswith('*'):
            linea = actividades.readline()
        if linea == '':
            break
        miro = linea.split(sep = ',')
        miro[1] = miro[1].strip()
        if miro[1] == 'B':
            while not linea.startswith('*'):
                linea = actividades.readline()
            linea = actividades.readline()
        elif miro[1] == 'A':
            linea = actividades.readline()
            while not linea.startswith('+'):
                linea = actividades.readline()
            linea = actividades.readline()
            miro = linea.split(sep = ',')
            if not miro[0] == idusuario:
                while not linea.startswith('*'):
                    linea = actividades.readline()
                linea = actividades.readline()
            elif miro[0] == idusuario:
                while not linea.startswith('-'):
                    linea = actividades.readline()
                linea = actividades.readline()
                while not linea.startswith('*'):
                    deudor = linea.split(sep = ',')
                    deudor[2] = deudor[2].strip()
                    if (deudor[0] in dictdeudores) and int(deudor[2]):
                        dictdeudores[deudor[0]] = dictdeudores[deudor[0]] + float(deudor[1])
                    elif not (deudor[0] in dictdeudores) and int(deudor[2]):
                        dictdeudores[deudor[0]] = float(deudor[1])
                    linea = actividades.readline()
    return dictdeudores

def aquienledebo(actividades: TextIO, idusuario: str) -> Dict[str, float]:
        linea = actividades.readline()
        dictacreed = {}
        while not linea == '':
            while linea.startswith('#') or linea.startswith('*'):
                linea = actividades.readline()
            if linea == '':
                break
            miro = linea.split(sep = ',')
            miro[1] = miro[1].strip()
            if miro[1] == 'B':
                while not linea.startswith('*'):
                    linea = actividades.readline()
                linea = actividades.readline()
            elif miro[1] == 'A':
                while not linea.startswith('+'):
                    linea = actividades.readline()
                linea = actividades.readline()
                posibleacreedor = linea.split(sep=',')[0]
                while not linea.startswith('-'):
                    linea = actividades.readline()
                linea = actividades.readline()
                deudor = linea.split(sep=',')
                deudor[2] = deudor[2].strip()
                while not deudor[0] == idusuario and not linea.startswith('*'):
                    linea = actividades.readline()
                    deudor = linea.split(sep=',')
                    if deudor[0].strip() == '*':
                        break
                    deudor[2] = deudor[2].strip()
                if deudor[0] == idusuario:
                    if (posibleacreedor in dictacreed) and int(deudor[2]):
                        dictacreed[posibleacreedor] = dictacreed[posibleacreedor] + float(deudor[1])
                    elif not (deudor[0] in dictacreed) and int(deudor[2]):
                        dictacreed[posibleacreedor] = float(deudor[1])
                    linea = actividades.readline()
                    while not linea.startswith('*'):
                        linea = actividades.readline()
                else:
                    linea = actividades.readline()
        return dictacreed


def creararchivocondicion(condicionusuario: TextIO,idusuario: str) -> None:
    condicionusuario.write('#Condicion de usuario ' + idusuario + '\n#Formato:\n#' + idusuario +'\n#+ (Quien le debe y cuanto)\n#ID de usuario,monto\n#...\n#- (A quien le debe y cuanto)\n#ID de usuario,monto\n#...\n#* (Marca final)\n' + idusuario + '\n+\n')
    with open('archivosdetexto/actividades.txt','r') as actividades:
        deudores = quienmedebe(actividades,idusuario)
    if not deudores == {}:
        for id,monto in deudores.items():
            condicionusuario.write(id + ',' + str(monto) + '\n')
    condicionusuario.write('-\n')
    with open('archivosdetexto/actividades.txt','r') as actividades:
        acreedores = aquienledebo(actividades,idusuario)
    if not acreedores == {}:
        for id,monto in acreedores.items():
            condicionusuario.write(id + ',' + str(monto) + '\n')
    condicionusuario.write('*\n')


if __name__ == '__main__':
    if not path.exists('archivosdetexto/actividades.txt'):
        inicio(True)
    with open('archivosdetexto/temporal.txt') as temporaldeusuario:
        generararcdeusuario(temporaldeusuario)
    if path.exists('archivosdetexto/archivodeusuario.txt'):
        with open('archivosdetexto/archivodeusuario.txt','r') as arcdeusuario:
            usuario = gestiondeusuario(arcdeusuario)
    datosusuario = buscarusuario(usuario)
    with open('archivosdetexto/condiciones/cond'+datosusuario[3]+datosusuario[0]+'.txt','w') as condicionusuario:
        creararchivocondicion(condicionusuario,datosusuario[3])
