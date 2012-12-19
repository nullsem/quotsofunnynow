#!/usr/bin/env bash

# provide a different work directory than default (/opt/quotsofunnynow)
workdir=$1

# get current directory
current=`pwd`

# enforce default if not user input
if [ -z "$workdir" ]; then
    workdir=/opt/
    echo "Using default directory '$workdir' ..."
fi

# check to see if leftovers from previous
# installation still exist
if ! [ -e $workdir ]; then
    echo "WARNING: Installation directory '$workdir' exists already. Overwriting..."
    rm -rf $workdir
fi

# install to directory
cp -r $current/ $workdir/

if ! [ $? -eq 0 ]; then
    echo "ERROR: Could not move '$current' to '$workdir'. Please resolve and try again..."
    exit $?
fi

# setup launcher
touch /usr/bin/quotsofunnynow
echo "#!/usr/bin/env bash" > /usr/bin/quotsofunnynow
echo >> /usr/bin/quotsofunnynow
echo "cd $workdir/quotsofunnynow" >> /usr/bin/quotsofunnynow
echo  >> /usr/bin/quotsofunnynow
echo "./quotsofunnynow.py" >> /usr/bin/quotsofunnynow

chmod +x /usr/bin/quotsofunnynow

quotsofunnynow
