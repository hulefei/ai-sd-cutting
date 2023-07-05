echo "run cutting from docker"

echo "NAME: $1"
echo "MODEL_NAME: $2"
echo "URL: $3"
echo "INDEX: $4"
echo "AUTO_SLICING: $5"

echo "run crop from docker"

docker run --rm \
-v /cfs/stable_diffusion/dreambooth/session:/app/session \
-e NAME=$1 \
-e MODEL_NAME=$2 \
-e URL=$3 \
-e INDEX=$4 \crop
-e AUTO_SLICING=$5 \
hulefei/cutting:latest
