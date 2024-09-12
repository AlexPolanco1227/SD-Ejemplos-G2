import java.util.concurrent.Semaphore;

class NumberPrinter {
    //Líneas del código donde se realiza la cooperación entre hilos
    private final Semaphore oddSemaphore = new Semaphore(1);    // Controla los impares
    private final Semaphore evenSemaphore = new Semaphore(0);   // Controla los pares
    private final Semaphore multipleOfThreeSemaphore = new Semaphore(0); // Controla los múltiplos de 3

    // Método para imprimir números impares
    void printOdd(int number) throws InterruptedException {
        oddSemaphore.acquire(); // Esperar turno para imprimir impar
        System.out.println("Impar: " + number);
        multipleOfThreeSemaphore.release(); // Ceder turno a los múltiplos de 3
    }

    // Método para imprimir números pares
    void printEven(int number) throws InterruptedException {
        evenSemaphore.acquire(); // Esperar turno para imprimir par
        System.out.println("Par: " + number);
        oddSemaphore.release(); // Ceder turno a los impares
    }

    // Método para imprimir múltiplos de 3
    void printMultipleOfThree(int number) throws InterruptedException {
        multipleOfThreeSemaphore.acquire(); // Esperar turno para imprimir múltiplo de 3
        System.out.println("Múltiplo de 3: " + number);
        evenSemaphore.release(); // Ceder turno a los pares
    }
}

public class Main {
    public static void main(String[] args) {
        NumberPrinter printer = new NumberPrinter();

        // Hilo que imprime números impares
        Thread oddThread = new Thread(() -> {
            for (int i = 1; i <= 19; i += 2) {
                try {
                    printer.printOdd(i);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        // Hilo que imprime números pares
        Thread evenThread = new Thread(() -> {
            for (int i = 2; i <= 20; i += 2) {
                try {
                    printer.printEven(i);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        // Hilo que imprime múltiplos de 3
        Thread multipleOfThreeThread = new Thread(() -> {
            for (int i = 3; i <= 18; i += 3) {
                try {
                    printer.printMultipleOfThree(i);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        // Iniciar los hilos
        oddThread.start();
        evenThread.start();
        multipleOfThreeThread.start();
    }
}
