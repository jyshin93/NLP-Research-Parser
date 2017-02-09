import java.util.HashTable;

public class FindDup {

	public static void deleteDup(LinkedListNode n) {
		HashTable table = new HashTable();
		LinkedListNode previous = null;
		while(n != null) {
			if (table.containsKey(n.data)) {
				previous.next = n.next;
			} else {
				table.put(n.data, true);
				previous = n;
			}
			n = n.next;
		}
	}
}

public static LinkedListNode nthToLast(LinkedListNode n, int k) {
	if (n == null) {
		return null;
	}
	if (k <= 0) {
		return null;
	}
	LinkedListNode pointer1 = n;
	LinkedListNode pointer2 = n;

	for (int i = 0; i < k - 1; i++) {
		if (pointer1 == null) {
			return null;
		}
		pointer1 = pointer1.next;
	}
	if (pointer1 == null) {
		return null;
	}
	while(pointer1 != null) {
		pointer1 = pointer1.next;
		pointer2 = pointer2.next;
	}
	return pointer2;
}

public static boolean deleteNode(LinkedListNode n) {
	if (n == null || n.next == null) {
		return false;
	}
	LinkedListNode next = n.next;
	n.data = next.data;
	n.next = next.next;
	return true;
}