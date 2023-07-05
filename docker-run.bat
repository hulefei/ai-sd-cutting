@echo off

echo "run cutting from docker"
docker run ^
-v testvolume:/app/session ^
-e NAME=lefeihu ^
-e MODEL_NAME=test_4 ^
-e URL=https://media.discordapp.net/attachments/1099559127195340854/1124232247873110057/icewolf29_police_officer_0a2fdb75-e9e6-4ea0-901c-0a7e9806597f.png ^
-e SAVE_TO=session ^
-e INDEX=0 ^
-e AUTO_SLICING=True ^
hulefei/cutting:latest
