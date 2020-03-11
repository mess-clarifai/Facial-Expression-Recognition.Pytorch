FILE_ID=1Oy_9YmpkSKX1Q8jkOhJbz3Mc7qjyISzU
FILE_NAME="FER2013_VGG19/PrivateTest_model.t7"

mkdir -p FER2013_VGG19

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=$FILE_ID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$FILE_ID" -O $FILE_NAME && rm -rf /tmp/cookies.txt
