#!/bin/sh

(echo .mode csv titanic; echo .import out.csv titanic; echo .quit) | sqlite3 titanic.db