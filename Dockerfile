FROM matsengrp/cpp

RUN apt-get update && apt-get install -y --no-install-recommends \
    doxygen \
    graphviz \
    texinfo

COPY . /bpp
WORKDIR /bpp
RUN python get_latest_bpp.py
ENV LD_LIBRARY_PATH /usr/local/lib
