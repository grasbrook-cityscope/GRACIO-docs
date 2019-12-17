
#!/bin/bash
# to be executed in ~/city-scope-grasbrook/modules
#for i in {0..6}; ## doesnt work on the VM's bash
for i in `seq 0 6`;
do
  # initiate nth noise docker
  cd noise
  sh ./docker/run_docker.sh $i &
  echo "Started noise docker $i"
  cd ..
  # initiate nth KPI docker
  cd pyGraKPI
  sh ./run.sh $i &
  echo "Started KPI docker $i"
  cd ..
  # initiate nth walkability docker
  cd pyWaFFill
  sh ./run.sh $i &
  echo "Started walkability docker $i"
  cd ..
# initiate nth stormwater docker
  cd pyStoCS
  sh ./run.sh $i &
  echo "Started stormwater docker $i"
  cd ..
done

docker ps

