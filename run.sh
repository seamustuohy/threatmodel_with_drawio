#!/usr/bin/env bash
#
# Copyright © 2018 seamus tuohy, <code@seamustuohy.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the included LICENSE file for details.

# Setup

#Bash should terminate in case a command or chain of command finishes with a non-zero exit status.
#Terminate the script in case an uninitialized variable is accessed.
#See: https://github.com/azet/community_bash_style_guide#style-conventions
set -e
set -u

# TODO remove DEBUGGING
# set -x

# Read Only variables

readonly PROG_DIR=$(readlink -m $(dirname $0))
# readonly PROGNAME="$( cd "$( dirname "BASH_SOURCE[0]" )" && pwd )"

readonly image_name="s2e/drawio"
readonly instance_name="drawio"

main() {
    if [[ "$run_command" == "bash" ]]; then
        run_command="bash"
    else
        run_command="draw.io"
    fi

    local DOCKER_DIR=/tmp/docker_file_transfer
    mkdir -p /tmp/docker_file_transfer
    echo "Place import files for draw.io into $DOCKER_DIR and extract your diagram from there after you finish."

    local state=$(docker inspect --format "{{.State.Running}}" "${instance_name}" 2>/dev/null)
    if [[ "$state" == "true" ]]; then
        docker stop "${instance_name}"
    fi

    docker run \
       --rm -it \
       -v /etc/localtime:/etc/localtime:ro \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -e "DISPLAY=unix${DISPLAY}" \
       -e GDK_SCALE \
       -e GDK_DPI_SCALE \
       -v "${DOCKER_DIR}:/root/imported_files" \
       --name "${instance_name}" \
       "${image_name}" "${run_command}"
}


build() {
    docker build --rm --force-rm -t "${image_name}" .
}

# check for positional param without unbound exception set
set +u
run_command="$1"
set -u
if [[ "$run_command" == "bash" ]]; then
    main bash
elif [[ "$run_command" == "build" ]]; then
    build
elif [[ "$run_command" == "csv" ]]; then
    # echo "${PROG_DIR}"
    python3 "${PROG_DIR}/create_attack_tree.py" -i "$2"
else
    main
fi
