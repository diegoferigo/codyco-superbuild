# BFL
include(YCMEPHelper)
include(FindOrBuildPackage)

if(${CODYCO_USES_OROCOS_BFL_BERDY})
    set(CODYCO_CMAKE_CACHE_ARGS_USER_DEFINED ${CODYCO_CMAKE_CACHE_ARGS_USER_DEFINED} -DCODYCO_USES_OROCOS_BFL_BERDY:BOOL=ON)
elseif()
    set(CODYCO_CMAKE_CACHE_ARGS_USER_DEFINED ${CODYCO_CMAKE_CACHE_ARGS_USER_DEFINED} -DCODYCO_USES_OROCOS_BFL_BERDY:BOOL=OFF)
endif()


ycm_ep_helper(orocosBFLBerdy TYPE GIT
              STYLE GITHUB
              REPOSITORY jeljaik/orocos-bfl-berdy
              TAG master
              COMPONENT libraries
              CMAKE_CACHE_ARGS ${CODYCO_CMAKE_CACHE_ARGS_USER_DEFINED}
              DEPENDS YARP)
