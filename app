npx create-expo-app ./
npm run reset-project
npx expo start
tsx to jsx
npx expo install @react-navigation/drawer

// _layout.jsx
import { Ionicons } from "@expo/vector-icons";
import { Drawer } from "expo-router/drawer";

export default function RootLayout() {
  return (
    <Drawer
      screenOptions={{
        headerStyle: { backgroundColor: "#14b8a6" },
        headerTintColor: "rgba(255, 255, 255, 1)",
        drawerActiveTintColor: "#14b8a6",
        drawerInactiveTintColor: "gray",
        drawerLabelStyle: { fontSize: 16 },
      }}
    >
      <Drawer.Screen
        name="index"
        options={{
          title: "Home",
          drawerIcon: ({ color, size }) => (
            <Ionicons name="home-outline" size={size} color={color} />
          ),
        }}
      />
      
      <Drawer.Screen
        name="products"
        options={{
          title: "Products",
          drawerIcon: ({ color, size }) => (
            <Ionicons name="apps-outline" size={size} color={color} />
          ),
        }}
      />
      
      <Drawer.Screen
        name="alert"
        options={{
          title: "Alert",
          drawerIcon: ({ color, size }) => (
            <Ionicons name="notifications-outline" size={size} color={color} />
          ),
        }}
      />

      <Drawer.Screen
        name="info"
        options={{
          title: "Info",
          drawerIcon: ({ color, size }) => (
            <Ionicons name="information-circle-outline" size={size} color={color} />
          ),
        }}
      />
    </Drawer>
  );
}



// alert.jsx
import { Ionicons } from "@expo/vector-icons";
import { useState } from "react";
import { Alert, StyleSheet, Text, TouchableOpacity, View } from "react-native";

export default function AlertScreen() {
  const [notifications, setNotifications] = useState(true);

  const showAlert = () => {
    Alert.alert(
      "Notification Settings",
      "Choose how you want to receive notifications",
      [
        { text: "Cancel", style: "cancel" },
        { text: "Enable", onPress: () => setNotifications(true), style: "default" },
        { text: "Disable", onPress: () => setNotifications(false), style: "destructive" },
      ]
    );
  };

  return (
    <View style={styles.container}>
      <Ionicons 
        name={notifications ? "notifications" : "notifications-off"} 
        size={70} 
        color="#14b8a6" 
      />
      <Text style={styles.title}>Notifications</Text>
      <Text style={styles.status}>Status: {notifications ? "Enabled" : "Disabled"}</Text>
      
      <TouchableOpacity style={styles.btn} onPress={showAlert}>
        <Text style={styles.btnText}>Change Settings</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: "#f5f5f5" },
  title: { fontSize: 24, fontWeight: "700", marginTop: 20, marginBottom: 8 },
  status: { fontSize: 16, color: "#666", marginBottom: 30 },
  btn: { backgroundColor: "#14b8a6", paddingHorizontal: 24, paddingVertical: 12, borderRadius: 8 },
  btnText: { color: "#fff", fontSize: 16, fontWeight: "600" },
});



// index.jsx
import { Ionicons } from "@expo/vector-icons";
import { StyleSheet, Text, View } from "react-native";

export default function Index() {
  return (
    <View style={styles.container}>
      <Ionicons name="home" size={70} color="#14b8a6" />
      <Text style={styles.title}>Welcome</Text>
      <Text style={styles.subtitle}>Open the menu to navigate</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: "#f5f5f5" },
  title: { fontSize: 24, fontWeight: "700", marginTop: 20, marginBottom: 8 },
  subtitle: { fontSize: 15, color: "#666" },
});



// info.jsx
import { Ionicons } from "@expo/vector-icons";
import { Platform, StyleSheet, Text, View } from "react-native";

export default function InfoScreen() {
  const osName = Platform.OS === "ios" 
    ? "iOS" 
    : Platform.OS === "android" 
    ? "Android" 
    : Platform.OS;
    
  const version = Platform.OS === "android" 
    ? `API ${Platform.Version}` 
    : `${Platform.Version}`;
    
  const icon = Platform.OS === "ios" 
    ? "logo-apple" 
    : Platform.OS === "android" 
    ? "logo-android" 
    : "help-circle";

  return (
    <View style={styles.container}>
      <Ionicons name={icon} size={70} color="#14b8a6" />
      <Text style={styles.title}>System Info</Text>

      <View style={styles.card}>
        <View style={styles.row}>
          <Text style={styles.label}>Operating System:</Text>
          <Text style={styles.value}>{osName}</Text>
        </View>
        <View style={styles.divider} />
        <View style={styles.row}>
          <Text style={styles.label}>Version:</Text>
          <Text style={styles.value}>{version}</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    justifyContent: "center", 
    alignItems: "center", 
    backgroundColor: "#f5f5f5", 
    padding: 20 
  },
  title: { fontSize: 24, fontWeight: "700", marginTop: 20, marginBottom: 30 },
  card: { 
    backgroundColor: "#fff", 
    borderRadius: 12, 
    padding: 20, 
    width: "100%", 
    elevation: 3 
  },
  row: { 
    flexDirection: "row", 
    justifyContent: "space-between", 
    paddingVertical: 10 
  },
  label: { fontSize: 15, color: "#666" },
  value: { fontSize: 16, color: "#14b8a6", fontWeight: "700" },
  divider: { height: 1, backgroundColor: "#e0e0e0", marginVertical: 8 },
});


// products.jsx
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  Image,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

export default function ProductsScreen() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://dummyjson.com/products")
      .then((res) => res.json())
      .then((data) => {
        setProducts(data.products);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <Image source={{ uri: item.thumbnail }} style={styles.img} resizeMode="cover" />
      <View style={{ padding: 12 }}>
        <Text style={styles.title} numberOfLines={2}>{item.title}</Text>
        <Text style={styles.desc} numberOfLines={3}>{item.description}</Text>
        
        <View style={styles.row}>
          <Text style={styles.price}>${item.price}</Text>
          <Text style={styles.rating}>⭐ {item.rating.toFixed(1)}</Text>
        </View>

        <TouchableOpacity
          style={styles.btn}
          onPress={() => console.log(`Added ${item.title} to cart`)}
          activeOpacity={0.8}
        >
          <Text style={styles.btnText}>Add to Cart</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#14b8a6" />
      </View>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: "#f5f5f5" }}>
      <FlatList
        data={products}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderItem}
        contentContainerStyle={{ padding: 12 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  card: { backgroundColor: "#fff", marginBottom: 12, borderRadius: 8, overflow: "hidden", elevation: 3 },
  img: { width: "100%", height: 200 },
  title: { fontSize: 16, fontWeight: "700", marginBottom: 6 },
  desc: { fontSize: 13, color: "#666", marginBottom: 10 },
  row: { flexDirection: "row", justifyContent: "space-between", marginBottom: 10 },
  price: { fontSize: 16, fontWeight: "700", color: "#14b8a6" },
  rating: { fontSize: 14, color: "#ff9800" },
  btn: { backgroundColor: "#14b8a6", paddingVertical: 10, borderRadius: 6, alignItems: "center" },
  btnText: { color: "#fff", fontSize: 14, fontWeight: "600" },
});


