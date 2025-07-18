#!/bin/sh

# Copyright 2022 The Cobalt Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

TOOLS_VERSION="${1:-6200805}"
TOOLS_FILENAME="commandlinetools-linux-${TOOLS_VERSION}_latest.zip"
BASE_URL="https://dl.google.com/android/repository"
ANDROID_SDK_ROOT="${ANDROID_HOME:-${HOME}/starboard-toolchains/AndroidSdk}"
SDK_MANAGER_TOOL="${ANDROID_SDK_ROOT}/cmdline-tools/1.0/bin/sdkmanager"
CURRENT_WORKING_DIRECTORY="${PWD}"

if [ ! -f "${SDK_MANAGER_TOOL}" ]; then
  echo "Downloading the SDK..."

  rm -rf "${ANDROID_SDK_ROOT}"

  cd /tmp
  mkdir -p ${ANDROID_SDK_ROOT}
  curl --silent -O -J  ${BASE_URL}/${TOOLS_FILENAME}
  unzip ${TOOLS_FILENAME} -d ${ANDROID_SDK_ROOT}
  rm ${TOOLS_FILENAME}
  mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools
  mv ${ANDROID_SDK_ROOT}/tools ${ANDROID_SDK_ROOT}/cmdline-tools/1.0
  echo "Android SDK installed."
fi

cd "${CURRENT_WORKING_DIRECTORY}"

echo "Updating the SDK..."

# Accept all SDK licenses non-interactively
yes | ${SDK_MANAGER_TOOL} --sdk_root=${ANDROID_SDK_ROOT} --update || true
yes | ${SDK_MANAGER_TOOL} --sdk_root=${ANDROID_SDK_ROOT} --licenses || true

# Update the installation
${SDK_MANAGER_TOOL} --sdk_root=${ANDROID_SDK_ROOT} \
    "build-tools;31.0.0" \
    "build-tools;34.0.0" \
    "cmake;3.22.1" \
    "cmdline-tools;1.0" \
    "extras;android;m2repository" \
    "extras;google;m2repository" \
    "ndk;25.2.9519653" \
    "platforms;android-31" \
    "platforms;android-34" \
    "platform-tools"

echo "Android SDK updated."
