#!/bin/bash
set -e

cd "$SRC_DIR/backend-dev/composer_container"

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
docker build -t $COMPOSER_REPO_NAME .
docker tag $COMPOSER_REPO_NAME:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$COMPOSER_REPO_NAME:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$COMPOSER_REPO_NAME:latest

cd "$SRC_DIR/backend-dev/provider_container"

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
docker build -t $PROVIDER_REPO_NAME .
docker tag $PROVIDER_REPO_NAME:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$PROVIDER_REPO_NAME:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$PROVIDER_REPO_NAME:latest

cd "$SRC_DIR"