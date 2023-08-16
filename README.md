# DGSW-Fighter
실행 시 주의사항

1. 실행 전 brew로 libmediainfo를 설치하셔야 합니다.

2. 혹시 실행에 오류가 난다면 pygame, ffpyplayer, pymediainfo 모두 정상적으로 설치됐는지 확인해 주세요.

3. 그래도 오류가 나면 아마도 libmediainfo 환경 변수가 vsc에서 지정되지 않아서일 것입니다.
vsc 콘솔 창에서
export DYLD_LIBRARY_PATH=/System/Volumes/Data/opt/homebrew/lib:/opt/homebrew/lib:$DYLD_LIBRARY_PATH
를 입력하시면 정상적으로 실행됩니다.
