#!/bin/bash
#usage : ./run.sh [実行回数] [検索ワード]
#集まる総ツイート数は実行回数 * 回数ごとのツイート収集数(config.iniのTWEET_COUNT)

#pip install and load libraries
FILE=./venv/bin/activate
if [ ! -f $FILE ];
then
    echo "creating new virtualenv...[venv]"
    virtualenv venv --no-site-package
fi
echo "activate virtualenv & pip install "
source ./venv/bin/activate
pip install -r requirements.txt

#run
for i in $(seq 1 $1)
do
    python gettweet.py $2
    wait
done

#write a tweet textfile from db json file 
python db2file.py
rm ./output/db.json
deactivate
