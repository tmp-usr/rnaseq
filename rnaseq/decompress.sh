#!/bin/bash

if [ $# -lt 1 ];then
	echo "[usage] $0 file.bz2"
	exit 1
fi

bzip2 -dk $1

