cmake_minimum_required(VERSION 3.26)
project(Agreg_Papi)

set(CMAKE_CXX_STANDARD 17)

# Trouver la bibliothèque libcurl
find_package(CURL REQUIRED)
find_library(COCOA_LIBRARY Cocoa)
find_library(FOUNDATION_LIBRARY Foundation)
find_library(USER_NOTIFICATIONS_LIBRARY UserNotifications)


add_executable(Agreg_Papi main.cpp
        notification.mm)

# Lier la bibliothèque libcurl à votre exécutable
target_link_libraries(Agreg_Papi PRIVATE CURL::libcurl
        ${COCOA_LIBRARY}
        ${FOUNDATION_LIBRARY}
        ${USER_NOTIFICATIONS_LIBRARY})

# Définir le bundle ID (identifiant unique) de votre application
set_target_properties(Agreg_Papi PROPERTIES
        BUNDLE True
        MACOSX_BUNDLE_BUNDLE_NAME "Agreg_Papi"  # Nom de votre application
        MACOSX_BUNDLE_BUNDLE_VERSION "1.0"       # Version de votre application
        MACOSX_BUNDLE_BUNDLE_GUI_IDENTIFIER "com.monentreprise.AgregPapi"  # Bundle ID
        MACOSX_BUNDLE_ICON_FILE "icone.icns"     # Icône de l'application
)