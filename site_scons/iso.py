#
# Copyright (C) 2009 Niek Linnenbank
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import tempfile
import version

from build import *
from SCons.Script import *

#
# Generate an ISO 9660 image.
# TODO: using 'cp' directly may be unportable.
#
def generateISO(target, source, env):

    # Open the list.
    list = open(str(source[0]))
    
    # Create a temporary directory.
    temp = tempfile.mkdtemp()
    
    # Read out which file to add.
    for line in list.readlines():

	# Copy them to the temporary directory.
	os.system("cp --parents '" + line.strip() + "' '" + temp + "'")

    # Create an bootable ISO image.
    os.system("mkisofs -R -b boot/grub/stage2_eltorito -no-emul-boot " +
	      "        -boot-load-size 4 -boot-info-table -V 'FreeNOS " + version.release + "'" +
	      "        -o " + str(target[0]) + " " + temp)

    # Done.
    os.system("rm -rf " + temp)
    list.close()

isoBuilder = Builder(action     = generateISO,
	    	     suffix     = '.iso',
		     src_suffix = '.isodesc')

target.Append(BUILDERS = { 'ISO' : isoBuilder })

isoImage = target.ISO('#boot/boot.iso', ['#boot/boot.isodesc'])
Depends(isoImage, ['bin', 'lib', 'kernel', 'sbin', 'srv', '#boot/boot.ext2'])
Alias('iso', isoImage)
AlwaysBuild(isoImage)
