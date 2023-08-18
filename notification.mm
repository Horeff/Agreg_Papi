#import <Foundation/Foundation.h>
#import <UserNotifications/UserNotifications.h>

extern "C" void sendNotification(const char* text, const char* path) {
    @autoreleasepool {
        // Créer une instance de NSUserNotification
        NSUserNotification *notification = [[NSUserNotification alloc] init];
        notification.title = @"La Champagne Viticole";
        notification.informativeText = [NSString stringWithUTF8String:text];

        // Ajouter une icône à la notification
        NSString *iconPath = [NSString stringWithFormat:@"%s/icone.png", path];
        NSImage *icon = [[NSImage alloc] initWithContentsOfFile:iconPath];
        notification.contentImage = icon;

        // Afficher la notification
        NSUserNotificationCenter *center = [NSUserNotificationCenter defaultUserNotificationCenter];
        [center deliverNotification:notification];
    }
}
