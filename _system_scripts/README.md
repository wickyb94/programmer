# Preperation

Assuming a blank stretch lite image from raspbian:

- raspi-config, enable ssh, enable auto login.
- you can use this command to find the pi on the network  
    ```
    sudo nmap -sn 10.27.8.0/24 | grep -r Raspberry -B 3
    ```


- get the USB dongle to mount.
    - Go to /etc/fstab and add this line:
        ```
        LABEL=PROGGERCODE       /media/programmer_code_dongle      vfat    defaults,noatime,nofail,ro      0       0
        ```
   
    
- set the config file to get the pin layout of your progger:
    ```
    echo 2 > ~/programmer_pin_version
    ```
   
    - Set the 2 to the matching number. You can find the supported maps in repo/lib/GpioMap
    
- reboot
    
- insert the USB drive and run 
    ```
    sudo /media/programmer_code_dongle/_system_scripts/dependenciesInstaller.sh
    ```
- then run 
    ```
    source /media/programmer_code_dongle/_system_scripts/copyOps.sh
    ```
    There will be a reboot.
    
- ensure that the service starts on boot without ssh.

- finally, when everything has been tested REALLY WELL, run the read-only-fs.sh in the danger folder
    ```
    sudo /media/programmer_code_dongle/_system_scripts/danger/read-only-fs.sh
    ```