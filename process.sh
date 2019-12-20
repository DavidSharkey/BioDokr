#!/bin/bash

# This shell scipt is involved in processing inputs (recieved from GUI) and managing communication between Docker containers. 
# It also creates an output folder and creates additional files in this folder.

# Removes spaces from $@ and puts each paramter into array param
param=($(echo $@ | tr " " "\n"))


input=""

# Obtains name of input from path.
name=${input##*/}
save_dir=""

# Set 
interproscan=false


#Augustus paramters
organism=${param[0]}
strand=${param[1]}
genemodel=${param[2]}


#InterProScan paramters
filex=""

cd $save_dir
mkdir Output
folder=/Output/
new_dir=$save_dir$folder

aug_file=$new_dir$Gff


cd $new_dir
# Makes results.txt in Ouput folder
echo "BioDokr Results/Analysis:" > results.txt



if [ ${#param[@]} = 5 ] && [ ${param[3]} == 'interproscan' ]; then

	interproscan=true
	filex=${param[4]}

fi

if [ ${#param[@]} = 6 ]; then
	
	karyotic=${param[4]}
fi

if [ ${#param[@]} = 6 ] && [ ${param[3]} = 'interproscan' ]; then

	interproscan=true
	filex=${param[4]}
fi

if [ ${#param[@]} = 7 ]; then

	interproscan=true
	filex=${param[4]}
	karyotic=${param[6]}
fi

if [ ${#param[@]} = 8 ]; then

	interproscan=true
	filex=${param[4]}
	karyotic=${param[6]}
fi



# Augustus 

cd /home/me/Desktop/BioDokr/dockerfiles/Augustus

# Build/Compile Dockerfile
docker build -t augustus . 

# Start container
docker run augustus --species=$organism --strand=$strand --genemodel=$genemodel $name

# Put information regarding running and stopped containers into "id.txt"
docker ps -a > /home/me/Desktop/BioDokr/id.txt

# augustusID is the ID of the container used, found at the 3rd row 1st column of id.txt
augustusID=`awk 'NR > 1 && NR < 3 {print $1}' /home/me/Desktop/BioDokr/id.txt`

# Transfer input file to the container
docker cp $input $augustusID:/

# Restart container and redirect output to new file in Output folder in host filesystem.
docker start -ai $augustusID > $aug_file



# getAnnoFasta.pl 

cd /home/me/Desktop/BioDokr/dockerfiles/Anno

docker build -t anno . 

docker run -it anno output.gff

docker ps -a > /home/me/Desktop/BioDokr/id.txt

annoID=`awk 'NR > 1 && NR < 3 {print $1}' /home/me/Desktop/BioDokr/id.txt`

docker cp $aug_file $annoID:/

docker start -ai $annoID

sudo docker cp $annoID:/output.aa $new_dir

cd $new_dir

count=`awk '/>/ {count=count+1} END {print count}' output.aa`

echo "There were" $count "genes/sequences found in" $name >> results.txt



#Interproscan

if [ $interproscan = true ]; then

cp $new_dir$AA /home/me/Desktop/BioDokr/dockerfiles/Interproscan/

cd /home/me/Desktop/BioDokr/dockerfiles/Interproscan

docker build -t interproscan . 

docker run -it interproscan -i output.aa --applications=pfam --goterms -f $filex 

docker ps -a > /home/me/Desktop/BioDokr/id.txt

interproScan=`awk 'NR > 1 && NR < 3 {print $1}' /home/me/Desktop/BioDokr/id.txt`

docker cp $interproScan:/interproscan-5.27-66.0/output.aa.$filex $new_dir

fi





