# /bin/bash

echo "Loading environment variables from .env file..."
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found. Please create one with the required variables."
  exit 1
fi

echo "Starting the Docker container with the following parameters:"
echo "LLAMACPP_IMAGE: $LLAMACPP_IMAGE"
echo "LLAMACPP_PORT: $LLAMACPP_PORT"
echo "LLAMACPP_HOST: $LLAMACPP_HOST"
echo "HOST_PORT: $HOST_PORT"
echo "MODELS_DIR: $MODELS_DIR"

echo "Running Docker container..."
sudo docker run -it --gpus all \
-v $MODELS_DIR:/models \
--security-opt=label=disable -p $HOST_PORT:$HOST_PORT $LLAMACPP_IMAGE \
-m /models/$GGUF_FILE \
--metrics \
--port $LLAMACPP_PORT --host $LLAMACPP_HOST 

# /whatever/llama.cpp/llava-cli -m /whatever/moondream2-text-model-f16.gguf --mmproj /whatever/moondream2-mmproj-f16.gguf  --image /whatever/picture.jpg -p "describe the image" --temp 0.1 -c 2048