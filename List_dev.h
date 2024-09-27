#ifndef DEVICE_DISCOVERY_H
#define DEVICE_DISCOVERY_H

#ifdef _WIN32
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT
#endif

extern "C" DLL_EXPORT const char* __cdecl GetDeviceList();

#endif // DEVICE_DISCOVERY_H
