#usage : ./run.sh [実行回数] [検索ワード]
#集まる総ツイート数は実行回数 * 回数ごとのツイート収集数(config.iniのTWEET_COUNT)

#pip install and load libraries
source venv/bin/activate
pip install -r requirement.txt

#run
for i in 'seq 1 $1'
do
    python gettweet.py $2
    wait
done

#write a tweet textfile from db json file 
python db2file.py
