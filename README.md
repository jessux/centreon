# Centreon batch pour la gestion des hôtes

## Objectif
L'objectif de ce batch est l'import en masse d'hosts dans Centreon en utilisant son API

## Configuration
Pour fonctionner, le batch a besoins de certains éléments de configuration dans le fichier config.py :
```python
#Centreon URL
URL="http://192.168.1.201"
#Centreon restApi user/password
USERNAME="REST"
PASSWORD="restAPI"
#Path to the file
LOG_FILENAME="log"
#console, file, both
LOG_TYPE="console"
#DEBUG,INFO,WARNING,ERROR,CRITICAL
LOG_LEVEL=logging.INFO
#Centreon restAPI TOKEN
TOKEN=""
```

## Fonctionnement
Pour fonctionner, le batch utilise un fichier plat (pour le moment)

###### Pour l'ajout d'hôtes :

------------

Nom;Alias;IP;Template;Poller;Hostgroup

------------

    1;1;1.1.1.1;OS-Linux-SNMP-custom;Central;Linux-Servers
    2;2;1.1.1.2;OS-Linux-SNMP-custom;Central;Linux-Servers
    3;3;1.1.1.3;OS-Linux-SNMP-custom;Central;Linux-Servers
    4;4;1.1.1.4;OS-Linux-SNMP-custom;Central;Linux-Servers
    5;5;1.1.1.5;OS-Linux-SNMP-custom;Central;Linux-Servers
    6;6;1.1.1.6;OS-Linux-SNMP-custom;Central;Linux-Servers

###### Pour la suppression d'hôtes :
------------
Nom

------------

    1
    2
    3
    4
    5
    6

## Execution du batch
Pour lancer le batch, il faut utiliser python 2.7 et taper :
```Shell
python import_hosts.py <file> <add|del>
```

##Evolutions prévues
- L'utilisation de l'API Netbox automatiquement à la place d'un fichier plat

