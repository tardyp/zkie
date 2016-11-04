zkie
====
Simple tool to access zookeeper configuration from the commandline, with syntax highlight.

.. code:: bash

    pip install 'zkie[ui]'


to install minimal command line without highlight, you can just use:

.. code:: bash

    pip install 'zkie'


Usage
=====

.. code:: bash

    # list all nodes recursively
    zk find /

    # upload myconfig.json to config directory
    zk upload myconfig.json /config/

    # display myconfig.json with syntax highlight
    zk get /config/myconfig.json

    # list directory
    zk ls /config
