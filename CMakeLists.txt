cmake_minimum_required(VERSION 3.0)
project(wordle_solver2)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

include_directories(jsoncpp/include)
find_library(JSONCPP_LIBRARY jsoncpp PATHS jsoncpp/build/debug/src/lib_json)
add_executable(main main.cpp)
target_link_libraries(main ${JSONCPP_LIBRARY})

